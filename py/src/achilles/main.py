#
# (C) 2023 zoidtechnologies.com All Rights Reserved.
#

import os
import pwd
import copy
import tempfile
import argparse

import getdate
import ttyio5 as ttyio
import bbsengine5 as bbsengine

import libachilles

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
    ttyio.echo("** needs save **")
  if ttyio.inputboolean("add fooditem? [yN]: ", "N") is True:
    ttyio.echo("...code to add fooditem...")
  return

def _edit(args, record, mode="edit"):
  editrecord = copy.deepcopy(record)

  done = False
  while not done:
    ttyio.echo("[U]PC:         ")
    ttyio.echo("[S]KU:         ")
    ttyio.echo("[N]ame:        %s" % (editrecord["name"]), end="")
    if record != editrecord:
      ttyio.echo(" (was: %s)" % (record["name"]))
    else:
      ttyio.echo()
    ttyio.echo("[T]itle:       %s" % (editrecord["title"]), end="")
    if record != editrecord:
      ttyio.echo(" (was: %s)" % (record["title"]))
    else:
      ttyio.echo()
    ttyio.echo("[I]ngredients: ")
    ttyio.echo("[F]rozen:      ")
    ttyio.echo("[D]escription  ")
    ttyio.echo("[M]anuf:       ")
    ttyio.echo("[L]ot:         ")
    ch = ttyio.inputchar("%s fooditem [USNTIDFM]: " % (mode), "USNTIDFMQ", "Q")
    if ch == "Q":
      ttyio.echo("Quit")
      break
    elif ch == "N":
      ttyio.echo("Name")
      editrecord["name"] = ttyio.inputstring("fooditem name: ", editrecord["name"])
    elif ch == "T":
      ttyio.echo("Title")
      editrecord["title"] = ttyio.inputstring("fooditem title: ", editrecord["title"])
  return editrecord

def setarea(args, left, stack=False):
  def right():
    currentmember = bbsengine.getcurrentmember(args)
    if currentmember is None:
      return ""
    rightbuf = "| %s | %s" % (currentmember["name"], bbsengine.pluralize(currentmember["credits"], "credit", "credits"))
    if args.debug is True:
      rightbuf += " | debug"
    return rightbuf
  bbsengine.setarea(left, right, stack)

def main(args):
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
    setarea(args, "achilles")
    bbsengine.title("achilles") # , hrcolor="{darkgreen}", titlecolor="{bggray}{white}")
    buf = ""
    for m in mainmenu:
      buf += "{bgdarkgray}{white}[{yellow}%s{white}]{/all} -- %s{F6}" % (m[0], m[1])
    buf += "{F6}{bgdarkgray}{white}[{yellow}Q{white}]{/all} -- Quit{F6}"
    ttyio.echo(buf)
    ch = ttyio.inputchar("achilles [LAKEQ]: {lightgreen}", "LAKEQ", "")
    if ch == "Q":
      ttyio.echo("Quit{/all}")
      done = True
      continue
    elif ch == "L":
      ttyio.echo("List{/all}")
    elif ch == "A":
      ttyio.echo("Add{/all}")
      add(args)
    elif ch == "E":
      ttyio.echo("Edit{/all}")
      edit(args)
  return

if __name__ == "__main__":
  ttyio.echo("{f6:3}{cursorup:3}") # curpos:%d,0}" % (ttyio.getterminalheight()-3))
  bbsengine.initscreen(bottommargin=1)

  parser = buildargs()
  args = parser.parse_args()

  try:
    main(args)
  except EOFError:
    ttyio.echo("{/all}{bold}EOF{/bold}")
  except KeyboardInterrupt:
    ttyio.echo("{/all}{bold}INTR{/bold}")
  finally:
    ttyio.echo("{decsc}{curpos:%d,0}{el}{decrc}{reset}{/all}" % (ttyio.getterminalheight()))
