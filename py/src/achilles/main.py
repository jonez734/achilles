#
# (C) 2023 zoidtechnologies.com All Rights Reserved.
#

import os
import pwd
import copy
import tempfile
import argparse

from bbsengine6 import io, screen, member, util

from . import lib

#membermap = {"jam" : 1}
#loginid = pwd.getpwuid(os.geteuid())[0]
#if loginid in membermap:
#  memberid = membermap[loginid]
#else:
#  memberid = None

def add(args):
  record = {}
  record["title"] = ""
  record["name"] = ""

  addrecord = _edit(args, record, "add")

  if record != addrecord:
    io.echo("** needs save **")
  if io.inputboolean("add fooditem? [yN]: ", "N") is True:
    io.echo("...code to add fooditem...")
  return

def _edit(args, record, mode="edit"):
  editrecord = copy.deepcopy(record)

  done = False
  while not done:
    io.echo("[U]PC:         ")
    io.echo("[S]KU:         ")
    io.echo("[N]ame:        %s" % (editrecord["name"]), end="")
    if record != editrecord:
      io.echo(" (was: %s)" % (record["name"]))
    else:
      io.echo()
    io.echo("[T]itle:       %s" % (editrecord["title"]), end="")
    if record != editrecord:
      io.echo(" (was: %s)" % (record["title"]))
    else:
      io.echo()
    io.echo("[I]ngredients: ")
    io.echo("[F]rozen:      ")
    io.echo("[D]escription  ")
    io.echo("[M]anuf:       ")
    io.echo("[L]ot:         ")
    ch = io.inputchar("%s fooditem [USNTIDFM]: " % (mode), "USNTIDFMQ", "Q")
    if ch == "Q":
      io.echo("Quit")
      break
    elif ch == "N":
      io.echo("Name")
      editrecord["name"] = io.inputstring("fooditem name: ", editrecord["name"])
    elif ch == "T":
      io.echo("Title")
      editrecord["title"] = io.inputstring("fooditem title: ", editrecord["title"])
  return editrecord

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

def init(args, **kw):
  return True

def access(args, op, **kw):
  return True

def buildargs(args=None, **kw):
  return None

def main(args, **kw):
  parser = lib.buildargs()
  args = parser.parse_args()

  mainmenu = (
    ("L", "List"),
    ("A", "Add"),
    ("K", "Kill"),
    ("E", "Edit")
  )
  done = False
  while not done:
    setarea(args, "achilles")
    screen.title("achilles") # , hrcolor="{darkgreen}", titlecolor="{bggray}{white}")
    buf = ""
    for m in mainmenu:
      buf += "{bgdarkgray}{white}[{yellow}%s{white}]{/all} -- %s{F6}" % (m[0], m[1])
    buf += "{F6}{bgdarkgray}{white}[{yellow}Q{white}]{/all} -- Quit{F6}"
    io.echo(buf)
    ch = io.inputchar("achilles [LAKEQ]: {lightgreen}", "LAKEQ", "")
    if ch == "Q":
      io.echo("Quit{/all}")
      done = True
      continue
    elif ch == "L":
      io.echo("List{/all}")
    elif ch == "A":
      io.echo("Add{/all}")
      add(args)
    elif ch == "E":
      io.echo("Edit{/all}")
      edit(args)
  return

