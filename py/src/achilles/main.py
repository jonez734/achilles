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

