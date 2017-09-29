#!/usr/bin/env python3

from __future__ import print_function

from webrelay.device.base import WebRelay_Page
from webrelay.device.base import WebRelay_Base

from webrelay.device.settings import Setting_IP
from webrelay.device.settings import Setting_Text
from webrelay.device.settings import Setting_Netspeed
from webrelay.device.settings import Setting_Netmode
from webrelay.device.settings import Setting_RelayMode
from webrelay.device.settings import Setting_Select
from webrelay.device.settings import Setting_Password
from webrelay.device.settings import Setting_YesNo
from webrelay.device.settings import Setting_TwoColor
from webrelay.device.settings import Setting_NumButtons

class NetworkPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Network')
        self.settings = [
            Setting_IP('IP Address', ['ipOne', 'ipTwo', 'ipThree', 'ipFour']),
            Setting_IP('Netmask', ['nmaskOne', 'nmaskTwo', 'nmaskThree', 'nmaskFour']),
            Setting_IP('Broadcast', ['bcastOctOne', 'bcastOctTwo', 'bcastOctThree', 'bcastOctFour']),
            Setting_IP('Gateway', ['gwOne', 'gwTwo', 'gwThree', 'gwFour']),
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

class RelayPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Relay/Input')
        self.settings = [
            Setting_RelayMode('Relay Mode', 'relayMode'),
            Setting_Text('Pulse Duration', 'pulseDur'),
            Setting_Select('Relay Options', 'relayOption'),
            Setting_Select('Remote Relay Options', 'rmtRelayOption'),
            Setting_IP('Remote Relay IP Address', ['rmtIpOne', 'rmtIpTwo', 'rmtIpThree', 'rmtIpFour']),
            Setting_Text('Remote TCP Port', 'rport'),
            Setting_Text('Relay #', 'relayNumber'),
            Setting_Select('Keep Alive', 'pingRmt'),
        ]

    def getPath(self):
        return '/relaySetup.html'

    def getUpdatePath(self):
        return '/relay.srv'

class ControlPage(WebRelay_Page):
    def __init__(self):
        super().__init__('Control Page Setup')
        self.settings = [
            Setting_Text('Main Header Text', 'headerTxt'),
            Setting_Text('Relay Description', 'relayDesc'),
            Setting_YesNo('Display Relay Status', 'dispRelayStat'),
            Setting_TwoColor('Status ON Color', 'statOnCol'),
            Setting_Text('Status ON Text', 'statOnTxt'),
            Setting_TwoColor('Status OFF Color', 'statOffCol'),
            Setting_Text('Status OFF Text', 'statOffTxt'),
            Setting_NumButtons('ON/OFF Buttons', 'numBttns'),
            Setting_Text('Button1 Label', 'bt1Label'),
            Setting_Text('Button2 Label', 'bt2Label'),
            Setting_YesNo('Pulse Button', 'pulsBttnOn'),
            Setting_Text('Pulse Button Label', 'pulsBtnLabel'),
            Setting_YesNo('Display Input Status', 'dispInpStat'),
            Setting_Text('Input Description', 'inpDesc'),
            Setting_TwoColor('Input ON Color', 'inputOnCol'),
            Setting_Text('Input ON Text', 'inpOnTxt'),
            Setting_TwoColor('Input OFF Color', 'inputOffCol'),
            Setting_Text('Input OFF Text', 'inpOffTxt'),
            Setting_YesNo('Auto Refresh Page', 'autoRefresh'),
            Setting_Text('Duration', 'refreshDur'),
        ]

    def getPath(self):
        return '/indexSetup.html'

    def getUpdatePath(self):
        return '/index1.srv'

class WebRelay1(WebRelay_Base):
    '''
    WebRelay X-WR-1R12-1I24-I

    # networkSetup.html
    # passwordSetup.html
    # relaySetup.html
    # indexSetup.html
    '''
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.pages = [
            NetworkPage(),
            PasswordPage(username, password),
            RelayPage(),
            ControlPage(),
        ]

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
