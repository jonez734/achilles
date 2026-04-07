from typing import Optional

from bbsengine6 import database, util

from . import select


def init(args, **kw: dict) -> Optional[bool]:
    return None


def access(args, op: str, **kw: dict) -> Optional[bool]:
    return None


def buildargs(args, **kw: dict) -> Optional[object]:
    return None


def main(args, **kw) -> None:
    util.heading("fooditem list")

    with database.connect(args) as pool:
        f = select(args, pool=pool)
        if f is not None:
            f.status()
    return
