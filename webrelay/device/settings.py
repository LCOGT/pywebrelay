#!/usr/bin/env python3

from __future__ import print_function
from collections import OrderedDict

def strtruncate(s, maxlength):
    '''
    Make sure the length of a string is less than a maximum length
    '''
    if len(s) > maxlength:
        return s[0:maxlength]

    return s

def exactly_one_element(result, elementtype, name):
    '''
    Make sure there is exactly one HTML element in the result array
    '''
    if len(result) <= 0:
        raise RuntimeError('Unable to find {} element with name: {}'.format(elementtype, name))

    if len(result) >= 2:
        raise RuntimeError('Found too many {} element with name: {}'.format(elementtype, name))

class Setting_Base(object):
    '''
    Base class for WebRelay Settings
    '''
    def __init__(self, name, formName):
        self.name = name
        self.formName = formName

        # Value on the device (current setting)
        self.deviceValue = None
        # Value that the user wants to set (updated setting)
        self.updateValue = None

    def __repr__(self):
        return repr(self.name)

    def needsUpdate(self):
        return not (self.deviceValue == self.updateValue)

    def getUpdateParams(self):
        if not self.needsUpdate():
            raise RuntimeError('No update needed for setting {}'.format(self.name))

        return {self.formName: self.updateValue, }

    def convertValueToHumanFormat(self, value):
        '''Convert a value in device-readable format into human-readable format'''
        # default to "no conversion necessary" mode
        return value

    def convertValueToDeviceFormat(self, value):
        '''Convert a value in human-readable format into device-readable format'''
        # default to "no conversion necessary" mode
        return value

    def fromSoup(self, soup):
        '''Fetch the information about this setting from the HTML soup'''
        raise RuntimeError('You forgot to implement the fromSoup() method')

    def toDict(self):
        '''Build a nested dictionary representing this setting'''
        humanValue = self.convertValueToHumanFormat(self.deviceValue)
        return OrderedDict({self.name: humanValue, })

    def fromDict(self, value):
        '''Set the new value (updated setting) in human-readable format'''
        self.updateValue = self.convertValueToDeviceFormat(value)

    def printDiff(self):
        '''Print a YAML-like unified diff of changed settings'''
        if self.needsUpdate():
            print('- {}: {}'.format(self.name, self.convertValueToHumanFormat(self.deviceValue)))
            print('+ {}: {}'.format(self.name, self.convertValueToHumanFormat(self.updateValue)))

    def fromSoup(self, soup):
        raise RuntimeError('You forgot to implement the fromSoup() method')

class Setting_Checkbox(Setting_Base):
    '''
    Class to handle a WebRelay check box setting.
    '''
    def __init__(self, name, formName):
        super().__init__(name, formName)

    def fromSoup(self, soup):
        attrs = {}
        attrs['name'] = self.formName
        attrs['type'] = 'checkbox'

        result = soup.find_all(name='input', attrs=attrs)
        exactly_one_element(result, 'input', self.formName)

        result = result[0]
        self.deviceValue = result.has_attr('checked')
        self.updateValue = self.deviceValue

class Setting_IP(Setting_Base):
    '''
    Class to handle a WebRelay IP Address type of setting. This includes
    things like IP Address, Netmask, Gateway, etc.

    The WebRelay treats this as four pieces of text input form data, each
    with their own form name (this varies significantly between each
    hardware variant).
    '''
    def __init__(self, name, formName):
        super().__init__(name, formName)

    def fromSoup(self, soup):
        ip = []
        for elem in self.formName:
            attrs = {}
            attrs['name'] = elem
            attrs['type'] = 'text'

            result = soup.find_all(name='input', attrs=attrs)
            exactly_one_element(result, 'input', elem)
            ip.append(result[0]['value'])

        self.deviceValue = '.'.join(ip)
        self.updateValue = self.deviceValue

    def getUpdateParams(self):
        ip = self.updateValue.split('.')
        return dict(zip(self.formName, ip))

class Setting_Select(Setting_Base):
    '''
    Class to handle a WebRelay select setting (a combo box).
    '''
    def __init__(self, name, formName):
        super().__init__(name, formName)
        self.deviceMap = {}

    def convertValueToHumanFormat(self, value):
        humanMap = {v: k for k, v in self.deviceMap.items()}
        return humanMap[value]

    def convertValueToDeviceFormat(self, value):
        return self.deviceMap[value]

    def fromSoup(self, soup):
        attrs = {}
        attrs['name'] = self.formName

        result = soup.find_all(name='select', attrs=attrs)
        exactly_one_element(result, 'select', self.formName)

        # remove any old data from the deviceMap
        self.deviceMap.clear()

        # fill the deviceMap with all options presented by the device
        result = result[0]
        for option in result.find_all(name='option'):
            option_value = option['value']
            option_text = option.text
            self.deviceMap[option_text] = option_value

            if option.has_attr('selected'):
                self.deviceValue = option_value
                self.updateValue = self.deviceValue

class Setting_Text(Setting_Base):
    '''
    Class to handle a WebRelay text setting (text input box).

    It automatically truncates the length of any updated settings to the
    length specified by the device.
    '''
    def __init__(self, name, formName):
        super().__init__(name, formName)
        self.maxLength = None

    def fromSoup(self, soup):
        attrs = {}
        attrs['name'] = self.formName
        attrs['type'] = 'text'

        result = soup.find_all(name='input', attrs=attrs)
        exactly_one_element(result, 'input', self.formName)
        result = result[0]

        # save maximum length if available
        if result.has_attr('maxlength'):
            self.maxLength = int(result['maxlength'])

        # save value from device
        self.deviceValue = result['value']
        self.updateValue = self.deviceValue

class Setting_Password(Setting_Base):
    '''
    Class to handle a WebRelay password setting (text input box).

    It automatically truncates the length of any updated settings to the
    length specified by the device.

    The password is optional, and only needed if this password is the
    password that controls access to the configuration pages.
    '''
    def __init__(self, name, formName, password=None):
        super().__init__(name, formName)
        self.maxLength = None
        self.password = password

    def fromSoup(self, soup):
        attrs = {}
        attrs['name'] = self.formName
        attrs['type'] = 'password'

        result = soup.find_all(name='input', attrs=attrs)
        exactly_one_element(result, 'input', self.formName)
        result = result[0]

        # save maximum length if available
        if result.has_attr('maxlength'):
            self.maxLength = int(result['maxlength'])

        # value from the HTML form
        value = result['value']

        # the device doesn't actually send the current password, it sends
        # a string of zeroes. Don't save this non-setting. Instead save
        # the real password used for authentication.
        if value == '0000000000':
            value = self.password

        self.deviceValue = value
        self.updateValue = self.deviceValue

class Setting_Radio(Setting_Base):
    '''
    Class to handle a WebRelay radio setting (choose exactly one of
    several settings).

    It doesn't automatically fetch all of the valid settings from the
    device. This is difficult or impossible due to the way radio buttons
    were implemented.
    '''

    # Map each possible radio button setting from Human format to
    # Device format. This should be overridden by subclasses to have
    # the specific options supported by the device.
    deviceMap = {}

    def __init__(self, name, formName):
        super().__init__(name, formName)

    def convertValueToHumanFormat(self, value):
        humanMap = {v: k for k, v in self.deviceMap.items()}
        return humanMap[value]

    def convertValueToDeviceFormat(self, value):
        return self.deviceMap[value]

    def fromSoup(self, soup):
        attrs = {}
        attrs['name'] = self.formName
        attrs['type'] = 'radio'

        result = soup.find_all(name='input', attrs=attrs)
        if len(result) <= 0:
            raise RuntimeError('Unable to find input radio element with name: {}'.format(self.formName))

        if len(result) <= 1:
            raise RuntimeError('Found too few input radio element with name: {}'.format(self.formName))

        self.deviceValue = None
        self.updateValue = self.deviceValue

        for idx, elem in enumerate(result):
            # skip un-selected elements
            if 'checked' not in elem.attrs:
                continue

            # save the device value from the HTML
            self.deviceValue = elem['value']
            self.updateValue = self.deviceValue

        if self.deviceValue is None:
            raise RuntimeError('Unable to find checked input radio element with name: {}'.format(self.formName))

class Setting_YesNo(Setting_Radio):
    deviceMap = {
        'Yes': 'yes',
        'No': 'no',
    }

class Setting_TwoColor(Setting_Radio):
    deviceMap = {
        'Gr': 'green',
        'Rd': 'red',
    }

class Setting_FourColor(Setting_Radio):
    deviceMap = {
        'Gr': 'green',
        'Rd': 'red',
        'Yllw': 'yellow',
        'Bl': 'blue',
    }

class Setting_NumButtons(Setting_Radio):
    deviceMap = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
    }

class Setting_RelayMode(Setting_Radio):
    deviceMap = {
        'Standard': 'relay',
        'Automatic Reboot': 'reboot',
    }

class Setting_Netspeed(Setting_Radio):
    deviceMap = {
        '10 Mbps': 'ten',
        '100 Mbps': 'hundred',
    }

class Setting_Netmode(Setting_Radio):
    deviceMap = {
        'Half Duplex': 'half',
        'Full Duplex': 'full',
    }

class Setting_EmailLength(Setting_Radio):
    deviceMap = {
        'Full Message': '0',
        'Short Message': '1',
    }

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
