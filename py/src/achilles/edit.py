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
        f = libfooditem.select(args, pool=pool)
        if f is None:
            return

        _fooditem = lib._edit(args, f, "edit")

        if (
            io.inputboolean(
                "{promptcolor}save changes? {optioncolor}[yN]{promptcolor}: {inputcolor}",
                "N",
            )
            is True
        ):
            _fooditem.datemodified = datetime.now()
            rec = _fooditem.buildrec()
            database.update(
                args,
                "achilles.__fooditem",
                _fooditem.id,
                rec,
                primarykey="id",
                conn=pool,
                commit=True,
            )
            io.echo(f"updated fooditem: {_fooditem.name}", level="info")
    return
