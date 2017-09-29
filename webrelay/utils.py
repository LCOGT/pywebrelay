#!/usr/bin/env python3

from __future__ import print_function

from webrelay.device import WebRelay1
from webrelay.device import WebRelay4
from webrelay.device import WebRelay6
from webrelay.device import WebRelay10

from collections import namedtuple

import requests
import logging
import bs4
import sys
import re

# Structure to hold WebRelay version information
VersionInfo = namedtuple('VersionInfo', [
    'modelNumber',
    'firmwareVersion',
    'serialNumber',
])

# Structure to hold WebRelay credentials
Credentials = namedtuple('Credentials', [
    'hostname',
    'username',
    'password',
])

def generate_authentication(username=None, password=None, password_file=None):
    '''
    Generate a list of authentication credentials for WebRelay devices.
    '''
    # Factory default username for all models is 'admin'
    if username is None:
        username = 'admin'

    # Factory default password for all models is 'webrelay'
    if password is None:
        password = 'webrelay'

    # Always use at least one set of credentials
    credentials = [(username, password), ]

    # Read additional passwords from a password file, if provided
    if password_file:
        with open(password_file, 'r') as f:
            for line in f.read().splitlines():
                credentials.append((username, line))

    # Return the list of possible credentials
    return credentials

def test_credentials(creds):
    '''
    Test if the given credentials is valid for configuring a WebRelay device.
    '''
    logging.debug('Testing Credentials: USER={} PASS={}'.format(creds.username, creds.password))

    try:
        url = 'http://{}/networkSetup.html'.format(creds.hostname)
        auth = requests.auth.HTTPBasicAuth(creds.username, creds.password)
        response = requests.get(url, auth=auth, timeout=10)

        # most models of device return 401 Unauthorized errors
        if response.status_code == 401:
            return False

        response.raise_for_status()
        return True
    except requests.exceptions.ConnectionError as ex:
        raise
    except Exception as ex:
        print('Unexpected Exception: {}'.format(str(ex)))
        return False

def detect_credentials(hostname, username=None, password=None, password_file=None):
    '''
    Generate a credentials list, and try them until a working set is found.
    '''
    # generate list of credentials to try
    credentials = generate_authentication(username, password, password_file)

    # test each set of credentials to see if we can authenticate successfully
    for username, password in credentials:
        try:
            creds = Credentials(hostname, username, password)
            success = test_credentials(creds)
            if success:
                logging.debug('Detected working credentials: USER={} PASS={}'.format(username, password))
                return creds
        except requests.exceptions.RequestException as ex:
            # die with an error message on any sort of network errors
            print('ERROR:', str(ex), file=sys.stderr)
            sys.exit(1)

    return None

def search_text(soup, pattern):
    '''
    Helper method to search the about.html/home.html page for version
    information.
    '''
    # WebRelay1 and WebRelay4 have their information within <p> elements
    # within a single table row. Try to find the information here first.
    for element in soup.find_all(name='p'):
        match = pattern.search(element.text)
        if match:
            return match

    # WebRelay6 and WebRelay10 have their information within <tr> elements,
    # one for each datum. Look here second.
    for element in soup.find_all(name='tr'):
        match = pattern.search(element.text)
        if match:
            return match

    # No match
    return None

def fetch_version_information(creds):
    '''
    Fetch the WebRelay version information into a VersionInfo structure.
    '''
    for path in ('about.html', 'home.html'):
        url = 'http://{}/{}'.format(creds.hostname, path)
        auth = requests.auth.HTTPBasicAuth(creds.username, creds.password)
        response = requests.get(url, auth=auth, timeout=10)

        # decode the content into a Python string
        content = response.content.decode('utf-8')

        # this page was not found
        if response.status_code == 404:
            continue

        # unfortunately, some variants of this device are mentally challenged,
        # and return a 200 response code with a 404 error in the content
        pattern = re.compile('404 Error')
        if pattern.search(content):
            continue

        # turn the whole page into plain text
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        # Model Number
        # WebRelay1 and WebRelay4 call this "Model"
        # WebRelay6 and WebRelay10 call this "Part Number"
        pattern = re.compile(r'(Model|Part Number):\s*(\S+)', re.IGNORECASE)
        match = search_text(soup, pattern)
        if not match:
            raise RuntimeError('Model Number not found')

        modelNumber = match.group(2)

        # Firmware Version
        # WebRelay1 and WebRelay4 call this "Product Revision"
        # WebRelay6 and WebRelay10 call this "Firmware Revision"
        pattern = re.compile(r'(Product|Firmware) Revision:\s*(\S+)', re.IGNORECASE)
        match = search_text(soup, pattern)
        if not match:
            raise RuntimeError('Firmware Version not found')

        firmwareVersion = match.group(2)

        # Serial Number
        # All variants call this "Serial Number"
        pattern = re.compile(r'Serial Number:\s*(\S+)', re.IGNORECASE)
        match = search_text(soup, pattern)
        if not match:
            raise RuntimeError('Serial Number not found')

        serialNumber = match.group(1)

        # return the structure
        return VersionInfo(modelNumber, firmwareVersion, serialNumber)

    # None of the possible information pages was accessible
    raise RuntimeError('Unable to fetch version information')

def get_webrelay_device(creds):
    '''
    Get the specialized device class for this WebRelay.
    '''
    info = fetch_version_information(creds)
    model = info.modelNumber

    # TODO FIXME: simplify
    hostname = creds.hostname
    username = creds.username
    password = creds.password

    if model.startswith('X-WR-1R'):
        return WebRelay1(hostname, username, password)
    elif model.startswith('X-WR-4R'):
        return WebRelay4(hostname, username, password)
    elif model.startswith('X-WR-6R'):
        return WebRelay6(hostname, username, password)
    elif model.startswith('X-WR-10R'):
        return WebRelay10(hostname, username, password)
    else:
        raise RuntimeError('Unsupported model {}'.format(model))

def setup_logging(level=logging.INFO, stream=sys.stdout):
    # get the default logger instance
    logger = logging.getLogger()

    # set the default output level
    logger.setLevel(level)

    # connect the logger to the requested stream
    ch = logging.StreamHandler(stream)

    # set the output format
    fmt = '%(asctime)s.%(msecs).03d %(levelname)7s: %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    # and hook it all together
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
