#!/usr/bin/env python3

from setuptools import setup

setup(
    name = 'pywebrelay',
    version = '1.0',
    description = 'Python Control of ControlByWeb WebRelay',
    url = 'https://github.com/LCOGT/pywebrelay/',
    author = 'Ira W. Snyder',
    author_email = 'isnyder@lco.global',
    license = 'MIT',
    packages = [
        'webrelay',
        'webrelay.device',
    ],
    install_requires = [
        'beautifulsoup4==4.8.0',
        'PyYAML==5.1',
        'requests==2.22.0',
        'netaddr==0.7.19',
    ],
    scripts = [
        'bin/webrelay_info',
        'bin/webrelay_fetch',
        'bin/webrelay_diff',
        'bin/webrelay_update',
        'bin/webrelay_bootstrap',
    ],
    zip_safe = True
)
