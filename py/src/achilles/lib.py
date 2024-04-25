#
# Copyright (C) 2024 zoidtechnologies.com. All Rights Reserved.
#
import argparse
from bbsengine6 import database, module, member, screen, util

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

def setarea(args, left, stack=False):
  def right():
    currentmember = member.getcurrent(args)
    if currentmember is None:
      return ""
    rightbuf = "| %s | %s" % (currentmember["moniker"], util.pluralize(currentmember["credits"], "credit", "credits"))
    if args.debug is True:
      rightbuf += " | debug"
    return rightbuf
  screen.setarea(left, right, stack)
