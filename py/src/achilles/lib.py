import argparse
import copy

from bbsengine6 import io, database, module, member, screen, util

from . import fooditem as libfooditem
from . import ui_schema


def buildargs(args=None, **kw):
    parser = argparse.ArgumentParser(prog="achilles")
    parser.add_argument(
        "--verbose", default=True, action="store_true", help="use verbose mode"
    )
    parser.add_argument(
        "--debug", default=False, action="store_true", help="run debug mode"
    )
    parser.add_argument(
        "--dry-run",
        dest="dryrun",
        action="store_true",
        default=True,
        help="dry run (no database changes)",
    )
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
        rightbuf = "| %s | %s" % (
            currentmember["moniker"],
            util.pluralize(currentmember["credits"], "credit", "credits"),
        )
        if args.debug is True:
            rightbuf += " | debug"
        return rightbuf

    screen.setarea(left, right, stack)


def _edit(args, fooditem, mode="edit"):
    _fooditem = copy.deepcopy(fooditem)

    done = False
    while not done:
        io.echo("{optioncolor}[U]{labelcolor} UPC:         ")
        io.echo("{optioncolor}[S]{labelcolor} SKU:         ")
        io.echo(
            f"{{optioncolor}}[N]{{labelcolor}} Name:        {{valuecolor}}{_fooditem.name}",
            end="",
        )
        if fooditem.name != _fooditem.name:
            io.echo(
                f"{{labelcolor}} (was: {{valuecolor}}{fooditem.name}{{labelcolor}})"
            )
        else:
            io.echo()
        io.echo(
            f"{{optioncolor}}[T]{{labelcolor}} Title:       {{valuecolor}}{_fooditem.title}",
            end="",
        )
        if fooditem.title != _fooditem.title:
            io.echo(
                f"{{labelcolor}} (was: {{valuecolor}}{fooditem.title}{{labelcolor}})"
            )
        else:
            io.echo()
        io.echo(
            f"{{optioncolor}}[M]{{labelcolor}} MSG Present: {{valuecolor}}{_fooditem.msgpresent}",
            end="",
        )
        if fooditem.msgpresent != _fooditem.msgpresent:
            io.echo(
                f"{{labelcolor}} (was: {{valuecolor}}{fooditem.msgpresent}{{labelcolor}})"
            )
        else:
            io.echo()
        io.echo(
            f"{{optioncolor}}[Q]{{labelcolor}} QSR:         {{valuecolor}}{_fooditem.qsr}",
            end="",
        )
        if fooditem.qsr != _fooditem.qsr:
            io.echo(
                f"{{labelcolor}} (was: {{valuecolor}}{fooditem.qsr}{{labelcolor}})"
            )
        else:
            io.echo()
        io.echo(
            f"{{optioncolor}}[F]{{labelcolor}} Frozen:      {{valuecolor}}{_fooditem.frozen}",
            end="",
        )
        if fooditem.frozen != _fooditem.frozen:
            io.echo(
                f"{{labelcolor}} (was: {{valuecolor}}{fooditem.frozen}{{labelcolor}})"
            )
        else:
            io.echo()
        io.echo("{optioncolor}[D]{labelcolor} Description  ")
        io.echo("{optioncolor}[L]{labelcolor} Lot:         ")

        ch = io.inputchar(
            f"{{promptcolor}}{mode} fooditem {{optioncolor}}[UNMTQF]{{promptcolor}}: {{inputcolor}}",
            "QXUNMTF",
            "Q",
        )
        if ch == "Q" or ch == "X":
            io.echo("Quit")
            break
        elif ch == "N":
            io.echo("Name")
            _fooditem.name = io.inputstring(
                "{promptcolor}fooditem name: {inputcolor}", _fooditem.name
            )
        elif ch == "T":
            io.echo("Title")
            _fooditem.title = io.inputstring(
                "{promptcolor}fooditem title: {inputcolor}", _fooditem.title
            )
        elif ch == "U":
            io.echo("UPC")
            _fooditem.upc = io.inputstring(
                "{promptcolor}fooditem UPC: {inputcolor}", _fooditem.upc
            )
        elif ch == "M":
            io.echo("MSG Present")
            _fooditem.msgpresent = io.inputboolean(
                "{promptcolor}MSG present? {optioncolor}[Yn]{promptcolor}: {inputcolor}",
                "Y" if _fooditem.msgpresent else "N",
            )
        elif ch == "Q":
            io.echo("QSR")
            _fooditem.qsr = io.inputboolean(
                "{promptcolor}Quick Service Restaurant? {optioncolor}[Yn]{promptcolor}: {inputcolor}",
                "Y" if _fooditem.qsr else "N",
            )
        elif ch == "F":
            io.echo("Frozen")
            _fooditem.frozen = io.inputboolean(
                "{promptcolor}frozen? {optioncolor}[Yn]{promptcolor}: {inputcolor}",
                "Y" if _fooditem.frozen else "N",
            )
    return _fooditem
