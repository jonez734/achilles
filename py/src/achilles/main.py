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
    io.echo(f"{{optioncolor}}[U]{{labelcolor}} UPC:         ")
    io.echo(f"{{optioncolor}}[S]{{labelcolor}} SKU:         ")
    io.echo(f"{{optioncolor}}[N]{{labelcolor}} Mame:        %s" % (editrecord["name"]), end="")
    if record != editrecord:
      io.echo(f" {{labelcolor}}(was: {{valuecolor}}{record['name']}{{labelcolor}})")
    else:
      io.echo()
    io.echo("[T]itle:       %s" % (editrecord["title"]), end="")
    if record != editrecord:
      io.echo(" (was: %s)" % (record["title"]))
    else:
      io.echo()
    io.echo(f"{{optioncolor}}[I]{{labelcolor}} Ingredients: ")
    io.echo(f"{{optioncolor}}[F]{{labelcolor}} Frozen:      ")
    io.echo(f"{{optioncolor}}[D]{{labelcolor}} Description  ")
    io.echo(f"{{optioncolor}}[M]{{labelcolor}} Manuf:       ")
    io.echo(f"{{optioncolor}}[L]{{labelcolor}} Lot:         ")
    ch = io.inputchar(f"{mode} fooditem {{optioncolor}}[USNTIDFM]{{promptcolor}}: {{inputcolor}}", "USNTIDFMXQ", "Q")
    if ch == "Q" or ch == "X":
      io.echo("Quit")
      break
    elif ch == "N":
      io.echo("Name")
      editrecord["name"] = io.inputstring("fooditem name: ", editrecord["name"])
    elif ch == "T":
      io.echo("Title")
      editrecord["title"] = io.inputstring("fooditem title: ", editrecord["title"])
  return editrecord


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
    lib.setarea(args, "achilles")
    screen.title("achilles: fooditems database") # , hrcolor="{darkgreen}", titlecolor="{bggray}{white}")
    util.heading("achilles: fooditem database")
    buf = ""
    for m in mainmenu:
      buf += f"{{optioncolor}}[{m[0]}]{{labelcolor}} {m[1]}{{F6}}"
    buf += "{F6}{optioncolor}[Q]{labelcolor} Quit{F6}"
    io.echo(buf)
    ch = io.inputchar("{promptcolor}achilles {optioncolor}[LAKEQ]{promptcolor}: {inputcolor}", "LAKEQX", "")
    if ch == "Q" or ch == "X":
      io.echo("Quit{/all}")
      done = True
    elif ch == "L":
      io.echo("List{/all}")
      lib.runmodule(args, "list")
    elif ch == "A":
      io.echo("Add{/all}")
      lib.runmodule(args, "add")
    elif ch == "E":
      io.echo("Edit{/all}")
      lib.runmodule(args, "edit")
    else:
      io.echo("{bell}")
  return

