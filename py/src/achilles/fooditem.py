import argparse
import copy
from datetime import datetime
from typing import Any, Optional

import dateutil.tz

from bbsengine6 import database, io, member, util
from bbsengine6.listboxcursor import ListboxCursor
from bbsengine6.listbox import ListboxItem, ListboxResult

ATTRIBUTES = {
    "upc": {"default": None},
    "sku": {"default": None},
    "lot": {"default": None},
    "serial": {"default": None},
    "name": {"default": None},
    "title": {"default": None},
    "description": {"default": None},
    "brandid": {"default": None},
    "manufid": {"default": None},
    "qsr": {"default": False},
    "msgpresent": {"default": False},
    "msgonlabel": {"default": False},
    "dsgpresent": {"default": False},
    "dsgonlabel": {"default": False},
    "frozen": {"default": False},
    "wic": {"default": False},
    "price": {"default": None},
    "quantity": {"default": None},
    "producturl": {"default": None},
    "datepurchased": {"default": None, "type": datetime},
    "dateposted": {"default": None, "type": datetime},
    "postedbymoniker": {"default": None},
    "datemodified": {"default": None, "type": datetime},
    "modifiedbymoniker": {"default": None},
}


class FoodItem:
    args: argparse.Namespace
    pool: Any
    conn: Any
    id: Optional[int]
    upc: Optional[str]
    sku: Optional[str]
    lot: Optional[str]
    serial: Optional[str]
    name: Optional[str]
    title: Optional[str]
    description: Optional[str]
    brandid: Optional[int]
    manufid: Optional[int]
    qsr: bool
    msgpresent: bool
    msgonlabel: bool
    dsgpresent: bool
    dsgonlabel: bool
    frozen: bool
    wic: bool
    price: Optional[float]
    quantity: Optional[str]
    producturl: Optional[str]
    datepurchased: Optional[datetime]
    dateposted: Optional[datetime]
    postedbymoniker: Optional[str]
    datemodified: Optional[datetime]
    modifiedbymoniker: Optional[str]

    def __init__(self, args, **kwargs):
        def _work(conn):
            self.attributes = copy.copy(ATTRIBUTES)
            for name, data in self.attributes.items():
                setattr(self, name, data["default"])
                self.attributes[name]["value"] = data["default"]

            self.debug = args.debug if hasattr(args, "debug") else False

        self.args = args
        self.id = kwargs.get("id", None)
        self.conn = kwargs.get("conn", None)
        self.pool = kwargs.get("pool", None)

        if self.conn is None:
            if self.pool is None:
                io.echo(f"achilles.FoodItem.__init__.100: {self.pool=}", level="error")
                return None
            with database.connect(args, pool=self.pool) as conn:
                return _work(conn)
        else:
            return _work(self.conn)

    def sync(self):
        for name in self.attributes.keys():
            self.setattributevalue(name, getattr(self, name))
        return True

    def verify_consistency(self, verbose=False) -> bool:
        consistent = True
        for name in self.attributes.keys():
            attr_val = getattr(self, name, None)
            attr_dict_val = self.attributes[name].get("value", None)
            if attr_val != attr_dict_val:
                consistent = False
                if verbose:
                    io.echo(
                        f"inconsistent attribute: {name}: attr={attr_val} != attributes['value']={attr_dict_val}",
                        level="warn",
                    )
        if verbose:
            if consistent:
                io.echo("verify_consistency: all values consistent", level="info")
            else:
                io.echo("verify_consistency: inconsistencies found", level="warn")
        return consistent

    def _validate_value(self, value, expected_type):
        if expected_type in (int, float) and value is not None:
            try:
                value = int(value)
            except (ValueError, TypeError):
                io.echo(f"invalid value: must be a number", level="error")
                return None, False
            if value < 0:
                io.echo("negative values not allowed", level="error")
                value = 0
        return value, True

    def _parse_datetime(self, value):
        if isinstance(value, str):
            try:
                from dateutil.parser import parse
                return parse(value)
            except Exception:
                pass
        return value

    def setattributevalue(self, name: str, value) -> bool:
        if name not in self.attributes:
            return False
        attr = self.attributes[name]
        expected_type = attr.get("type")
        if expected_type is None:
            if "value" in attr:
                expected_type = type(attr["value"])
            elif "default" in attr:
                expected_type = type(attr["default"])
            else:
                expected_type = str

        value, valid = self._validate_value(value, expected_type)
        if not valid:
            return False

        if expected_type is datetime:
            value = self._parse_datetime(value)

        self.attributes[name]["value"] = value
        setattr(self, name, value)
        return True

    def buildrec(self, **kwargs):
        rec = {}
        for name, data in self.attributes.items():
            if name in ("dateposted", "datemodified"):
                continue
            v = getattr(self, name, data["default"])
            if v is None:
                v = data["default"]
            rec[name] = database.convert_for_jsonb(v)
        return rec

    def update(self, conn, commit=True):
        def _work(conn):
            database.update(
                self.args,
                "achilles.__fooditem",
                self.id,
                self.buildrec(),
                primarykey="id",
                conn=conn,
                commit=commit,
            )
            return True

        if conn is None:
            io.echo(f"achilles.FoodItem.update.160: {conn=}", level="error")
            return False
        return _work(conn)

    def isdirty(self):
        dirty = False
        for name, data in self.attributes.items():
            if name in ("dateposted", "datemodified"):
                continue
            curval = getattr(self, name, None)
            oldval = data.get("value", data.get("default"))
            if curval != oldval:
                if self.debug:
                    io.echo(f"{name=} {curval=} {oldval=}", level="debug")
                dirty = True
        return dirty

    def save(self, force=False, commit=True):
        if self.args.debug:
            io.echo(f"FoodItem.save.100: {self.id=}", level="debug")
        if self.id is None:
            io.echo(f"fooditem id is not set. save aborted.", level="error")
            return None

        if force or self.isdirty():
            io.echo(
                f"{{var:labelcolor}}saving {{var:valuecolor}}{self.name}{{var:labelcolor}}: ",
                end="",
            )
            with database.connect(self.args, pool=self.pool) as conn:
                self.sync()
                self.update(conn, commit=commit)
            io.echo(" ok ", level="ok")
            return True

    def status(self):
        util.heading(f"fooditem status for {self.name}")
        terminal_width = io.terminal.width() - 2

        def format_value(value):
            if value is None:
                return ""
            if isinstance(value, bool):
                return "yes" if value else "no"
            elif isinstance(value, (int, float)):
                return f"{value}"
            elif isinstance(value, datetime):
                return value.strftime("%m/%d@%H:%M")
            else:
                return str(value)[:20]

        data = {}
        for name in self.attributes.keys():
            if name in ("dateposted", "datemodified"):
                continue
            data[name] = format_value(getattr(self, name, None))

        sorted_items = sorted(data.items())
        for label, value in sorted_items:
            io.echo(f"{{var:labelcolor}}{label:<20}: {{var:valuecolor}}{value}")
        util.hr()


def load(args, id: int, **kwargs) -> Optional[FoodItem]:
    def _work(conn):
        sql = "select * from achilles.__fooditem where id=%s"
        dat = (id,)

        with database.cursor(conn) as cur:
            cur.execute(sql, dat)
            if cur.rowcount == 0:
                io.echo(f"achilles.FoodItem.load.300: {id=} not found", level="info")
                return None

            rec = cur.fetchone()
            return build(args, rec, **kwargs)

    pool = kwargs.get("pool", None)
    if pool is None:
        io.echo(f"achilles.FoodItem.load.500: {pool=}", level="error")
        return None

    with database.connect(args, pool=pool) as conn:
        return _work(conn)


def build(args, rec: dict, **kwargs) -> FoodItem:
    f = FoodItem(args, **kwargs)
    for name, data in f.attributes.items():
        v = rec.get(name, data["default"])
        if v is None:
            v = data["default"]
        setattr(f, name, v)
    f.id = rec.get("id")
    return f


def exists(args, id: int, **kwargs) -> bool:
    def _work(conn):
        with database.cursor(conn) as cur:
            sql = "select 1 from achilles.__fooditem where id=%s"
            dat = (id,)
            cur.execute(sql, dat)
            if cur.rowcount == 0:
                return False
            return True

    pool = kwargs.get("pool", None)
    if pool is None:
        io.echo("exists.100: pool not passed", level="debug")
        with database.getpool(args) as pool:
            with database.connect(args, pool=pool) as conn:
                return _work(conn)
    else:
        with database.connect(args, pool=pool) as conn:
            return _work(conn)


def count(args, **kwargs) -> int:
    def _work(conn):
        sql = "select count(id) from achilles.__fooditem"
        with database.cursor(conn) as cur:
            cur.execute(sql, ())
            rec = cur.fetchone()
            if rec is None:
                return 0
            return rec["count"]

    conn = kwargs.get("conn", None)
    if conn is None:
        pool = kwargs.get("pool", None)
        if pool is None:
            io.echo("count.100: pool is None", level="error")
            return 0
        with database.connect(args, pool=pool) as conn:
            return _work(conn)
    else:
        return _work(conn)


def select(args, title: str = "select fooditem", prompt: str = "fooditem: ", **kwargs) -> Optional[FoodItem]:
    pool = kwargs.get("pool", None)
    if pool is None:
        io.echo(f"achilles.FoodItem.select.300: {pool=}", level="error")
        return None

    class FoodItemListbox(ListboxCursor):
        def __init__(self, args, **kwargs):
            self.pool = kwargs.get("pool", None)
            super().__init__(args, **kwargs)

    class FoodItemListboxItem(ListboxItem):
        def __init__(self, rec: dict, width: int):
            super().__init__()
            self.fooditem = build(args, rec)
            if self.fooditem is None:
                io.echo(f"FoodItem.select.240: {self.fooditem=}", level="error")
                return

            left = f"{self.fooditem.name}"
            right = f"MSG: {'Y' if self.fooditem.msgpresent else 'N'} | QSR: {'Y' if self.fooditem.qsr else 'N'}"
            rightlen = len(right)
            self.content = f"{left.ljust(width - rightlen - 10)}{right}"
            self.pk = self.fooditem.id
            self.data = {"fooditem": self.fooditem, "rec": rec}
            self.width = width

        def help(self):
            io.echo(
                f"{{var:labelcolor}}use {{var:valuecolor}}KEY_ENTER{{var:labelcolor}} to select"
            )

    with database.connect(args, pool=pool) as conn:
        sql = "select id, name, msgpresent, qsr from achilles.__fooditem order by name"
        dat = ()

        existingcount = count(args, pool=pool)
        with database.cursor(conn) as cur:
            cur.execute(sql, dat)
            FoodItemListbox.pool = pool
            lb = FoodItemListbox(
                args,
                title=title,
                totalitems=existingcount,
                cur=cur,
                itemclass=FoodItemListboxItem,
                pool=pool,
            )

            while True:
                op = lb.run(prompt)
                if op.status == "selected" and op.item:
                    return op.item.data["fooditem"]
                if op.status == "cancelled":
                    return None


def create(args, **kwargs) -> Optional[FoodItem]:
    pool = kwargs.get("pool", None)
    if pool is None:
        io.echo("achilles.FoodItem.create.140: pool is None", level="error")
        return False

    def _work(conn, name: str) -> FoodItem:
        f = FoodItem(args, pool=pool)
        f.name = name
        f.dateposted = datetime.now(dateutil.tz.tzlocal())

        rec = f.buildrec()
        rec["name"] = name
        rec["dateposted"] = f.dateposted

        database.insert(
            args,
            "achilles.__fooditem",
            rec,
            primarykey="id",
            conn=conn,
            commit=True,
        )

        sql = "select id from achilles.__fooditem where name=%s"
        with database.cursor(conn) as cur:
            cur.execute(sql, (name,))
            if cur.rowcount > 0:
                f.id = cur.fetchone()["id"]

        return f

    name = io.inputstring(
        "{promptcolor}fooditem name: {inputcolor}",
        "",
    )
    if name == "":
        io.echo("aborted.")
        return None

    try:
        conn = kwargs.get("conn", None)
        if conn is None:
            pool = kwargs.get("pool", None)
            if pool is None:
                io.echo("create.140: pool is None", level="error")
                return False
            with database.connect(args, pool=pool) as conn:
                return _work(conn, name)
        else:
            return _work(conn, name)
    except Exception as e:
        io.echo(f"achilles.FoodItem.create.100: exception {e}", level="error")
        raise
