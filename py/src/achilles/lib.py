#
# Copyright (C) 2024 zoidtechnologies.com. All Rights Reserved.
#
import argparse

def init(args=None):
    return True

def access(args, op, **kw):
    return True

def buildargs(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", dest="verbose")
    parser.add_argument("--debug", action="store_true", dest="debug")
    return parser
