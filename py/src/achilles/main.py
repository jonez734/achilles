from bbsengine6 import io, screen, util

from . import lib


def init(args, **kw):
    return None


def access(args, op, **kw):
    return True


def buildargs(args=None, **kw):
    return None


def main(args, **kw):
    parser = lib.buildargs()
    args = parser.parse_args()

    mainmenu = (("L", "List"), ("A", "Add"), ("K", "Kill"), ("E", "Edit"))
    done = False
    while not done:
        lib.setarea(args, "achilles")
        io.terminal.title("achilles: fooditems database")
        util.heading("achilles: fooditem database")
        buf = ""
        for m in mainmenu:
            buf += f"{{optioncolor}}[{m[0]}]{{labelcolor}} {m[1]}{{F6}}"
        buf += "{F6}{optioncolor}[Q]{labelcolor} Quit{F6}"
        io.echo(buf)
        ch = io.inputchar(
            "{promptcolor}achilles {optioncolor}[LAKEQ]{promptcolor}: {inputcolor}",
            "LAKEQX",
            "",
        )
        if ch == "Q" or ch == "X":
            io.echo("Quit{/all}")
            done = True
        elif ch == "L":
            io.echo("List{/all}")
            lib.runmodule(args, "fooditem.list")
        elif ch == "A":
            io.echo("Add{/all}")
            lib.runmodule(args, "fooditem.add")
        elif ch == "E":
            io.echo("Edit{/all}")
            lib.runmodule(args, "fooditem.edit")
        else:
            io.echo("{bell}")
    return
