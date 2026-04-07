import argparse
from datetime import datetime
from typing import Optional

from bbsengine6 import io, database

from . import select
from .tui import _edit


def init(args, **kw: dict) -> Optional[bool]:
    return None


def access(args, op: str, **kw: dict) -> Optional[bool]:
    return None


def buildargs(args, **kw: dict) -> Optional[argparse.ArgumentParser]:
    return None


def main(args, **kw):
    if args.dryrun:
        io.echo("{red}*** DRY RUN - no changes will be made ***{/all}")

    with database.connect(args) as pool:
        f = select(args, pool=pool)
        if f is None:
            return

        _fooditem = _edit(args, f, "edit")

        if io.inputboolean(
            "{promptcolor}save changes? {optioncolor}[yN]{promptcolor}: {inputcolor}",
            "N",
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
