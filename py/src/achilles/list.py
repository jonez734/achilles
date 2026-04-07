from bbsengine6 import io, database, util

from . import fooditem as libfooditem


def init(args, **kw: dict) -> bool:
    return True


def access(args, op: str, **kw: dict) -> bool:
    return True


def buildargs(args, **kw: dict):
    return None


def main(args, **kw):
    util.heading("fooditem list")

    with database.connect(args) as pool:
        f = libfooditem.select(args, pool=pool)
        if f is not None:
            f.status()
    return
