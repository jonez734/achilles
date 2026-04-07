from argparse import ArgumentParser
from datetime import datetime
from typing import Optional

from bbsengine6 import io, database

from . import fooditem as libfooditem
from . import lib


def init(args, **kw: dict) -> Optional[bool]:
    return None


def access(args, op: str, **kw: dict) -> Optional[bool]:
    return None


def buildargs(args, **kw: dict) -> Optional[ArgumentParser]:
    return None


def main(args, **kw):
    if args.dryrun:
        io.echo("{red}*** DRY RUN - no changes will be made ***{/all}")

    with database.connect(args) as pool:
        f = libfooditem.FoodItem(args, pool=pool)
        f.name = ""
        f.qsr = False
        f.msgpresent = False
        f.msgonlabel = False
        f.frozen = False
        f.wic = False

        _fooditem = lib._edit(args, f, "add")

        if f.name is None or f.name == "":
            io.echo("name is required", level="error")
            return

        if (
            io.inputboolean(
                "{promptcolor}add fooditem? {optioncolor}[yN]{promptcolor}: {inputcolor}",
                "N",
            )
            is True
        ):
            _fooditem.dateposted = datetime.now()
            rec = _fooditem.buildrec()
            database.insert(
                args,
                "achilles.__fooditem",
                rec,
                primarykey="id",
                conn=pool,
                commit=True,
            )
            io.echo(f"added fooditem: {_fooditem.name}", level="info")
    return
