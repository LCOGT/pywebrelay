#!/usr/bin/env python3

from __future__ import print_function

from collections import OrderedDict

import yaml
import sys

# https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def yaml_ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def dump_yaml(data):
    return yaml_ordered_dump(data, Dumper=yaml.SafeDumper, default_flow_style=False)

def read_yaml(stream):
        return yaml.load(stream)

def read_input_file(filename):
    # read from stdin if requested
    if filename == '-':
        return read_yaml(sys.stdin)

    # otherwise read from the file specified
    with open(filename, 'r') as f:
        return read_yaml(f)

def main():
    pass

if __name__ == '__main__':
    main()

# vim: set ts=4 sts=4 sw=4 et tw=120:
