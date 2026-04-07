from bbsengine6 import database, io
from typing import Optional

from . import FoodItem, select, create


def add(args, **kwargs) -> Optional[FoodItem]:
    return create(args, **kwargs)


def edit(args, **kwargs) -> Optional[FoodItem]:
    return select(args, **kwargs)


def list_items(args, **kwargs) -> Optional[FoodItem]:
    return select(args, **kwargs)


def delete(args, **kwargs) -> Optional[FoodItem]:
    f = select(args, **kwargs)
    if f is None:
        return None

    f.status()

    if io.inputboolean(
        "{promptcolor}delete fooditem? {optioncolor}[yN]{promptcolor}: {inputcolor}",
        "N",
    ):
        database.delete(
            args,
            "achilles.__fooditem",
            f.id,
            primarykey="id",
            conn=kwargs.get("conn"),
            commit=True,
        )
        io.echo(f"deleted fooditem: {f.name}", level="info")
        return f
    return None
