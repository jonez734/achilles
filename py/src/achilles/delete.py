from bbsengine6 import io, database

from . import fooditem as libfooditem


def init(args, **kw: dict) -> bool:
    return True


def access(args, op: str, **kw: dict) -> bool:
    return True


def buildargs(args, **kw: dict):
    return None


def main(args, **kw):
    if args.dryrun:
        io.echo("{red}*** DRY RUN - no changes will be made ***{/all}")

    with database.connect(args) as pool:
        f = libfooditem.select(args, pool=pool)
        if f is None:
            return

        f.status()

        if (
            io.inputboolean(
                "{promptcolor}delete fooditem? {optioncolor}[yN]{promptcolor}: {inputcolor}",
                "N",
            )
            is True
        ):
            database.delete(
                args,
                "achilles.__fooditem",
                f.id,
                primarykey="id",
                conn=pool,
                commit=True,
            )
            io.echo(f"deleted fooditem: {f.name}", level="info")
    return
