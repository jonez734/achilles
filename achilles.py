#
# (C) 2020 Zoid Technologies. All Rights Reserved.
#

import os
import pwd
import copy
import tempfile

from optparse import OptionParser

import ttyio4 as ttyio

import bbsengine4 as bbsengine

import libachilles

membermap = {"jam" : 1}
loginid = pwd.getpwuid(os.geteuid())[0]
if loginid in membermap:
  memberid = membermap[loginid]
else:
  memberid = None

def main():
    ttyio.echo("achilles")
    return

if __name__ == "__main__":
    main()
