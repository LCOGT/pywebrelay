#!/usr/bin/env python3

from __future__ import print_function

from webrelay.device.base import WebRelay_Page
from webrelay.device.base import WebRelay_Base

from webrelay.device.settings import Setting_IP
from webrelay.device.settings import Setting_Text
from webrelay.device.settings import Setting_Netspeed
from webrelay.device.settings import Setting_Netmode
from webrelay.device.settings import Setting_YesNo
from webrelay.device.settings import Setting_FourColor
from webrelay.device.settings import Setting_NumButtons
from webrelay.device.settings import Setting_Password

class NetworkPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Network')
        self.settings = [
            Setting_IP('IP Address', ['ip1', 'ip2', 'ip3', 'ip4']),
            Setting_IP('Netmask', ['nm1', 'nm2', 'nm3', 'nm4']),
            Setting_IP('Broadcast', ['bc1', 'bc2', 'bc3', 'bc4']),
            Setting_IP('Gateway', ['gw1', 'gw2', 'gw3', 'gw4']),
            Setting_Text('TCP Port', 'lport'),
            Setting_Text('Modbus Port', 'mbusport'),
            Setting_Netspeed('Speed', 'netSpeed'),
            Setting_Netmode('Mode', 'netMode'),
        ]

    def getPath(self):
        return '/networkSetup.html'

    def getUpdatePath(self):
        return '/network.srv'

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
        return '/password.srv'

    def passwordWasChanged(self):
        return self.settings[0].needsUpdate()

    def getNewPassword(self):
        return self.settings[0].updateValue

class ControlPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Control Page Setup')
        self.settings = [
            Setting_Text('Main Header Text', 'hT'),
            Setting_YesNo('Auto Refresh Page', 'autoRefresh'),
            Setting_Text('Duration', 'refreshDur'),
        ]

    def getPath(self):
        return '/relay1Setup.html'

    def getUpdatePath(self):
        return '/relay1Setup.srv'

class RelayPage(WebRelay_Page):
    def __init__(self, number):
        name = 'Relay {}'.format(number)
        super().__init__(name)
        self.number = number
        self.settings = [
            Setting_Text('Relay Description', 'rD'),
            Setting_YesNo('Display Relay Status', 'dRS'),
            Setting_FourColor('Status ON Color', 'sOnC'),
            Setting_Text('Status ON Text', 'sOnT'),
            Setting_FourColor('Status OFF Color', 'sOffC'),
            Setting_Text('Status OFF Text', 'sOffT'),
            Setting_NumButtons('ON/OFF Buttons', 'nB'),
            Setting_Text('Button1 Label', 'b1L'),
            Setting_Text('Button2 Label', 'b2L'),
            Setting_YesNo('Pulse Button', 'pB'),
            Setting_Text('Pulse Button Label', 'pBL'),
            Setting_Text('Pulse Duration', 'pulseDur'),
        ]

    def getPath(self):
        return '/relay{}Setup.html'.format(self.number)

    def getUpdatePath(self):
        return '/relay{}Setup.srv'.format(self.number)

class WebRelay4(WebRelay_Base):
    '''
    WebRelay X-WR-4R12-I

    # networkSetup.html
    # passwordSetup.html
    # relay1Setup.html
    # relay2Setup.html
    # relay3Setup.html
    # relay4Setup.html
    '''
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.pages = [
            NetworkPage(),
            PasswordPage(username, password),
            ControlPage(),
            RelayPage(1),
            RelayPage(2),
            RelayPage(3),
            RelayPage(4),
        ]

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
