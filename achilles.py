#
# (C) 2020 Zoid Technologies. All Rights Reserved.
#

import os
import pwd
import copy
import tempfile
import argparse

import getdate
import ttyio4 as ttyio
import bbsengine4 as bbsengine

import libachilles

membermap = {"jam" : 1}
loginid = pwd.getpwuid(os.geteuid())[0]
if loginid in membermap:
  memberid = membermap[loginid]
else:
  memberid = None

def add(args):
  pass

def main():
  parser = argparse.ArgumentParser(prog="achilles")
  parser.add_argument("--verbose", default=True, action="store_true", help="use verbose mode")
  parser.add_argument("--debug", default=False, action="store_true", help="run debug mode")
  parser.add_argument("--dry-run", dest="dryrun", action="store_true", default=True, help="dry run (no database changes)")
  # @todo: address 'zoidweb4' as hardcoded database name
  bbsengine.buildargdatabasegroup(parser)
  args = parser.parse_args()

  mainmenu = (
    ("L", "List"),
    ("A", "Add"),
    ("K", "Kill"),
    ("E", "Edit")
  )
  done = False
  while not done:
    bbsengine.title("achilles - food item - terminal interface", hrcolor="{green}", titlecolor="{bggray}{white}")
    buf = ""
    for m in mainmenu:
      buf += "{bgdarkgray}{white}[{yellow}%s{white}]{/all} -- %s{F6}" % (m[0], m[1])
    buf += "{F6}{bgdarkgray}{white}[{yellow}Q{white}]{/all} -- Quit{F6}"
    ttyio.echo(buf)
    try:
      ch = ttyio.inputchar("achilles main [LAKEQ]: {lightgreen}", "LAKEQ", "")
    except (EOFError, KeyboardInterrupt) as e:
      ttyio.echo("Quit")
      return
    finally:
      pass
      # ttyio.echo("{/all}")
    if ch == "Q":
      ttyio.echo("Quit")
      done = True
      continue
    elif ch == "L":
      ttyio.echo("List")
    elif ch == "A":
      ttyio.echo("Add")
      add()
    elif ch == "E":
      ttyio.echo("Edit")
      edit()
  return

if __name__ == "__main__":
    main()
