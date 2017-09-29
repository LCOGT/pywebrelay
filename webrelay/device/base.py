#!/usr/bin/env python3

from __future__ import print_function
from collections import OrderedDict

import requests
import logging
import bs4

class WebRelay_Page(object):
    '''
    Base class for WebRelay configuration page (HTML form).
    '''
    def __init__(self, name):
        self.name = name
        self.settings = []

    def getPath(self):
        '''Return the HTTP Path to the form to fetch the current settings'''
        raise RuntimeError('You forgot to implement the getPath() method')

    def getUpdatePath(self):
        '''Return the HTTP Path to the form to submit the updated settings'''
        raise RuntimeError('You forgot to implement the getUpdatePath() method')

    def getUpdateMethod(self):
        '''
        Return the HTTP Method used for update (GET/POST).

        Most or all of the variants of the WebRelay devices are mentally
        challenged, and use HTTP GET requests to update their state. A big
        no-no.
        '''
        return 'GET'

    def getUpdateParams(self):
        '''Return a dictionary of query parameters needing update'''
        if not self.needsUpdate():
            raise RuntimeError('No update was needed. No settings were changed.')

        params = {}
        for elem in self.settings:
            if elem.needsUpdate():
                params.update(elem.getUpdateParams())

        return params

    def needsUpdate(self):
        '''
        Does this configuration page need to update the device? Have any
        settings been changed by the user?
        '''
        for elem in self.settings:
            if elem.needsUpdate():
                return True

        return False

    def fromSoup(self, soup):
        '''Load all of the current settings from the device from BeautifulSoup'''
        for elem in self.settings:
            elem.fromSoup(soup)

    def toDict(self):
        '''Build a nested dictionary representing this page'''
        data = OrderedDict()
        for elem in self.settings:
            data.update(elem.toDict())

        return OrderedDict({self.name: data, })

    def fromDict(self, data):
        '''Update a page from a nested dictionary representing this page'''
        for elem in self.settings:
            if elem.name in data:
                elem.fromDict(data[elem.name])

    def printDiff(self):
        '''Print a YAML-like unified diff of changed settings'''
        if self.needsUpdate():
            print('{}:'.format(self.name))
            for elem in self.settings:
                elem.printDiff()

    def passwordWasChanged(self):
        '''
        Hook for password pages to indicate whether they changed the password
        used to update the settings. This is so we can start using the new
        password for all future requests.
        '''
        return False

    def getNewPassword(self):
        '''Return the new password that was just set onto the device'''
        raise RuntimeError('You forgot to implement the getNewPassword() method')

class WebRelay_Base(object):
    '''
    Base class for WebRelay devices.

    A WebRelay device consists of:
    - hostname / username / password
    - a set of configuration pages (HTML forms)
    '''
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.pages = []

    def loadFromDevice(self):
        '''Load all of the settings from the device into this object'''
        for page in self.pages:
            url = 'http://{}{}'.format(self.hostname, page.getPath())
            auth = requests.auth.HTTPBasicAuth(self.username, self.password)

            logging.debug('Fetch URL={} with USER={} PASS={}'.format(url, self.username, self.password))

            response = requests.get(url, auth=auth, timeout=10)
            response.raise_for_status()

            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            page.fromSoup(soup)

    def writeToDevice(self):
        '''Write all updated settings from this object onto the device'''
        if not self.needsUpdate():
            raise RuntimeError('You called writeToDevice() on a device without updates')

        for page in self.pages:
            if page.needsUpdate():
                # TODO FIXME: support something other than GET
                method = page.getUpdateMethod()
                if method != 'GET':
                    raise RuntimeError('HTTP methods other than GET are not yet supported')

                url = 'http://{}{}'.format(self.hostname, page.getUpdatePath())
                auth = requests.auth.HTTPBasicAuth(self.username, self.password)
                params = page.getUpdateParams()

                logging.debug('Write URL={} with USER={} PASS={}'.format(url, self.username, self.password))
                logging.debug('Parameters: {}'.format(params))

                response = requests.get(url, auth=auth, timeout=10, params=params)
                response.raise_for_status()

            # cleanly handle password updates in the middle of updating settings
            if page.passwordWasChanged():
                logging.debug('Password was changed, updating password used to access device')
                self.password = page.getNewPassword()

    def needsUpdate(self):
        '''Check if the device needs any settings saved back to it'''
        for page in self.pages:
            if page.needsUpdate():
                return True

        return False

    def toDict(self):
        '''Build a nested dictionary representing this device'''
        data = OrderedDict()
        for page in self.pages:
            data.update(page.toDict())

        return data

    def fromDict(self, data):
        '''Update a device from a nested dictionary representing this device'''
        for page in self.pages:
            if page.name in data:
                page.fromDict(data[page.name])

    def printDiff(self):
        '''Print a YAML-like unified diff of changed settings'''
        if self.needsUpdate():
            for page in self.pages:
                page.printDiff()

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
