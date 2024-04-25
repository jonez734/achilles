#
# Copyright (C) 2024 zoidtechnologies.com. All Rights Reserved.
#
import argparse
from bbsengine6 import database, module

def init(args=None):
    return True

def access(args, op, **kw):
    return True

def buildargs(args=None, **kw):
  parser = argparse.ArgumentParser(prog="achilles")
  parser.add_argument("--verbose", default=True, action="store_true", help="use verbose mode")
  parser.add_argument("--debug", default=False, action="store_true", help="run debug mode")
  parser.add_argument("--dry-run", dest="dryrun", action="store_true", default=True, help="dry run (no database changes)")
  database.buildargdatabasegroup(parser)
  return parser

def runmodule(args, modulename, **kw):
  return module.runmodule(args, f"achilles.{modulename}", **kw)

def checkmodule(args, modulename, **kw):
  return module.checkmodule(args, f"achilles.{modulename}", **kw)
