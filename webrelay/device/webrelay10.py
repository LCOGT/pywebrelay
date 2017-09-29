#!/usr/bin/env python3

from __future__ import print_function

from webrelay.device.base import WebRelay_Page
from webrelay.device.base import WebRelay_Base

from webrelay.device.settings import Setting_IP
from webrelay.device.settings import Setting_Text
from webrelay.device.settings import Setting_Netspeed
from webrelay.device.settings import Setting_Netmode
from webrelay.device.settings import Setting_Password
from webrelay.device.settings import Setting_Select
from webrelay.device.settings import Setting_Checkbox
from webrelay.device.settings import Setting_YesNo

class NetworkPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Network')
        self.settings = [
            Setting_IP('IP Address', ['ip1', 'ip2', 'ip3', 'ip4']),
            Setting_IP('Subnet Mask', ['nm1', 'nm2', 'nm3', 'nm4']),
            Setting_IP('Gateway', ['gw1', 'gw2', 'gw3', 'gw4']),
            Setting_IP('Preferred DNS Server', ['pdns1', 'pdns2', 'pdns3', 'pdns4']),
            Setting_IP('Alternate DNS Server', ['adns1', 'adns2', 'adns3', 'adns4']),
            Setting_Text('HTTP Port', 'lP'),
            Setting_Netspeed('Speed', 'nS'),
            Setting_Netmode('Mode', 'nM'),
            Setting_Text('Mail Server(SMTP)', 'sA'),
            Setting_Text('Mail Server Port', 'msp'),
            Setting_Text('User Name(If Required)', 'sUN'),
            Setting_Password('Password(If Required)', 'sP'),
            Setting_Text('Return Email', 'sndA'),
            Setting_Text('Email 1', 'email1'),
            Setting_Text('Email 2', 'email2'),
            Setting_Text('Email 3', 'email3'),
            Setting_Text('Email 4', 'email4'),
            Setting_Text('Email 5', 'email5'),
        ]

    def getPath(self):
        return '/networkSetup.html'

    def getUpdatePath(self):
        return '/networkSetup.srv'

class AdvancedNetworkPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Advanced Network')
        self.settings = [
            Setting_YesNo('Modbus Enabled', 'modEnbl'),
            Setting_Text('Modbus Port', 'mP'),
            Setting_YesNo('Remote Services Enabled', 'rmtSrvEnbled'),
            Setting_Text('Server Name/IP Address', 'rmtSrvName'),
            Setting_Text('Connection String', 'rmtSrvStr'),
            Setting_Text('Connection Interval', 'rmtSrvInt'),
            Setting_YesNo('SNMP Enabled', 'snmpEnbl'),
            Setting_IP('SNMP Manager IP', ['sip1', 'sip2', 'sip3', 'sip4']),
            Setting_Text('SNMP Port', 'snmpP'),
            Setting_Text('SNMP Trap Port', 'sTP'),
            Setting_IP('IP Filter Range 1 Low', ['ipRL11', 'ipRL12', 'ipRL13', 'ipRL14']),
            Setting_IP('IP Filter Range 1 High', ['ipRH11', 'ipRH12', 'ipRH13', 'ipRH14']),
            Setting_IP('IP Filter Range 2 Low', ['ipRL21', 'ipRL22', 'ipRL23', 'ipRL24']),
            Setting_IP('IP Filter Range 2 High', ['ipRH21', 'ipRH22', 'ipRH23', 'ipRH24']),
        ]

    def getPath(self):
        return '/rmtSrvSetup.html'

    def getUpdatePath(self):
        return '/rmtSrvSetup.srv'

class PasswordPage(WebRelay_Page):
    def __init__(self, username, password):
        super().__init__('Password')
        self.settings = [
            Setting_Password('Setup Password', 'setupPswd', password),
            Setting_Password('Re-enter Setup Password', 'setupPswdChk', password),
            Setting_YesNo('Enable Control Password', 'pswdEnbled'),
            Setting_Password('Control Password', 'ctrlPswd'),
            Setting_Password('Re-enter Control Password', 'ctrlPswdChk'),
        ]

    def getPath(self):
        return '/passwordSetup.html'

    def getUpdatePath(self):
        return '/passwordSetup.srv'

    def passwordWasChanged(self):
        return self.settings[0].needsUpdate()

    def getNewPassword(self):
        return self.settings[0].updateValue

class RelayPage(WebRelay_Page):
    def __init__(self, number):
        name = 'Relay {}'.format(number)
        super().__init__(name)
        self.number = number
        self.settings = [
            Setting_Text('Relay Description', 'rDesc'),
            Setting_Text('On Button Label', 'onbLbl'),
            Setting_Text('Off Button Label', 'offbLbl'),
            Setting_Text('Pulse Button Label', 'pbLbl'),
            Setting_Text('On Status Text', 'onLbl'),
            Setting_Text('Off Status Text', 'offLbl'),
            Setting_Text('Pulse Duration', 'pulseTime'),
            Setting_Select('Relay State At Powerup', 'rlyPwrState'),
            Setting_Select('Email Option', 'rlyEmailOpt'),
            Setting_Checkbox('Use Email Address 1', 'rem1'),
            Setting_Checkbox('Use Email Address 2', 'rem2'),
            Setting_Checkbox('Use Email Address 3', 'rem3'),
            Setting_Checkbox('Use Email Address 4', 'rem4'),
            Setting_Checkbox('Use Email Address 5', 'rem5'),
            Setting_Checkbox('Send State Msg/Trap on Relay Change', 'rmtEvnt'),
        ]

    def getPath(self):
        return '/relaychng.srv?rNum={}'.format(self.number)

    def getUpdatePath(self):
        return '/relaychng.srv'.format(self.number)

    def getUpdateParams(self):
        params = super().getUpdateParams()
        params.update({'rNum': self.number})

class ControlPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Control Page')
        self.settings = [
            Setting_Text('Main Header Text', 'headerTxt'),
            Setting_YesNo('Auto Refresh', 'autoRefresh'),
            Setting_Text('Refresh Rate', 'refreshRate'),
            Setting_Checkbox('Relay 1 Display State', 'dispR1'),
            Setting_Checkbox('Relay 1 Display On/Off Buttons', 'dispOOB1'),
            Setting_Checkbox('Relay 1 Display Pulse Button', 'dispPB1'),
            Setting_Checkbox('Relay 2 Display State', 'dispR2'),
            Setting_Checkbox('Relay 2 Display On/Off Buttons', 'dispOOB2'),
            Setting_Checkbox('Relay 2 Display Pulse Button', 'dispPB2'),
            Setting_Checkbox('Relay 3 Display State', 'dispR3'),
            Setting_Checkbox('Relay 3 Display On/Off Buttons', 'dispOOB3'),
            Setting_Checkbox('Relay 3 Display Pulse Button', 'dispPB3'),
            Setting_Checkbox('Relay 4 Display State', 'dispR4'),
            Setting_Checkbox('Relay 4 Display On/Off Buttons', 'dispOOB4'),
            Setting_Checkbox('Relay 4 Display Pulse Button', 'dispPB4'),
            Setting_Checkbox('Relay 5 Display State', 'dispR5'),
            Setting_Checkbox('Relay 5 Display On/Off Buttons', 'dispOOB5'),
            Setting_Checkbox('Relay 5 Display Pulse Button', 'dispPB5'),
            Setting_Checkbox('Relay 6 Display State', 'dispR6'),
            Setting_Checkbox('Relay 6 Display On/Off Buttons', 'dispOOB6'),
            Setting_Checkbox('Relay 6 Display Pulse Button', 'dispPB6'),
            Setting_Checkbox('Relay 7 Display State', 'dispR7'),
            Setting_Checkbox('Relay 7 Display On/Off Buttons', 'dispOOB7'),
            Setting_Checkbox('Relay 7 Display Pulse Button', 'dispPB7'),
            Setting_Checkbox('Relay 8 Display State', 'dispR8'),
            Setting_Checkbox('Relay 8 Display On/Off Buttons', 'dispOOB8'),
            Setting_Checkbox('Relay 8 Display Pulse Button', 'dispPB8'),
            Setting_Checkbox('Relay 9 Display State', 'dispR9'),
            Setting_Checkbox('Relay 9 Display On/Off Buttons', 'dispOOB9'),
            Setting_Checkbox('Relay 9 Display Pulse Button', 'dispPB9'),
            Setting_Checkbox('Relay 10 Display State', 'dispR:'),
            Setting_Checkbox('Relay 10 Display On/Off Buttons', 'dispOOB:'),
            Setting_Checkbox('Relay 10 Display Pulse Button', 'dispPB:'),
        ]

    def getPath(self):
        return '/controlPageSetup.html'

    def getUpdatePath(self):
        return '/controlPageSetup.srv'

class WebRelay10(WebRelay_Base):
    '''
    X-WR-10R12-I

    # networkSetup.html
    # rmtSrvSetup.html
    # passwordSetup.html
    # relaySetup.html -> relaychng.srv?rNum=1
    # relaySetup.html -> relaychng.srv?rNum=2
    # relaySetup.html -> relaychng.srv?rNum=3
    # relaySetup.html -> relaychng.srv?rNum=4
    # relaySetup.html -> relaychng.srv?rNum=5
    # relaySetup.html -> relaychng.srv?rNum=6
    # relaySetup.html -> relaychng.srv?rNum=7
    # relaySetup.html -> relaychng.srv?rNum=8
    # relaySetup.html -> relaychng.srv?rNum=9
    # relaySetup.html -> relaychng.srv?rNum=10
    # scriptSetup.html
    # controlPageSetup.html
    '''
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.pages = [
            NetworkPage(),
            AdvancedNetworkPage(),
            PasswordPage(username, password),
            RelayPage(1),
            RelayPage(2),
            RelayPage(3),
            RelayPage(4),
            RelayPage(5),
            RelayPage(6),
            RelayPage(7),
            RelayPage(8),
            RelayPage(9),
            RelayPage(10),
            ControlPage(),
        ]

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
