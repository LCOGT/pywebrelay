pywebrelay
==========

A Python module for automating the configuration of the
[ControlByWeb WebRelay](https://www.controlbyweb.com/webrelay/)
family of devices.

Requirements
------------
* [Python 3.5](http://python.org)

Python package requirements
---------------------------
* [PyYAML](https://pypi.python.org/pypi/PyYAML)
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/)
* [requests](https://pypi.python.org/pypi/requests/)
* [netaddr](https://pypi.python.org/pypi/netaddr)

Features
========

- Automatic detection of authentication credentials (passwords) from a password list.
- Fetch configuration from device and write to a file.
- Load new configuration from a file to a device.

Common Options
==============

Password File
-------------

The `--password-file` option takes a filename which contains one password per
line. The program will attempt to authenticate with each of these credentials
until it finds one that works.

Username / Password
-------------------

These are optional, and only necessary if you know the username and password
which is used for the device. It is a better idea to use the password file
feature.

Configuration File
------------------

The `--configuration-file` option takes a filename which contains updated
settings to load to a WebRelay device. Any ommitted options are simply ignored
when updating the device. This feature allows you to change some settings to
match a pre-defined template, while leaving other existing settings unchanged.

Tools
=====

`webrelay_info`
---------------

Detect authentication credentials and fetch basic information from a WebRelay
device.

`webrelay_fetch`
----------------

Fetch the current configuration from a WebRelay device and print it to standard
output in YAML format. This output can be saved to a file, edited, and then
loaded back to the WebRelay device using the `webrelay_update` tool.

`webrelay_diff`
---------------

Fetch the current configuration from a WebRelay device, and then print the
differences between the device and a configuration file.

`webrelay_update`
-----------------

Upload a new configuration to a WebRelay device.

`webrelay_bootstrap`
--------------------

The most versatile tool in the collection. Given a WebRelay device which has
been factory reset to it's default settings, this tool can perform the
following things:

- ARP spoofing to give the WebRelay device a temporary IP address.
- Upload a new configuration from a file to the WebRelay device.

Examples
========

Bootstrap a device from Factory settings
----------------------------------------

This will take a WebRelay device that has it's factory default settings, and
configure it with a temporary IP address and load settings from a configuration
file.

Required information:

- MAC Address (Serial Number)
- IP Address (temporary or permanent)
- New configuration file to load

    webrelay_bootstrap --sudo --macaddress 00:11:22:33:44:55 -i configuration.yml 1.2.3.4

Apply a configuration to a device
---------------------------------

This will take a WebRelay device and load updated settings from a
configuration file.

Required Information:

- IP Address or Hostname
- New configuration file to load

    webrelay_update -i configuration.yaml 1.2.3.4
