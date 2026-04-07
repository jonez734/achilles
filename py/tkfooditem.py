import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import argparse
from tkinter import (
    Tk,
    Frame,
    Button,
    Entry,
    Label,
    Checkbutton,
    BooleanVar,
    BOTH,
    X,
    LEFT,
    W,
)
from bbsengine6 import database

from achilles import fooditem as libfooditem
from achilles import ui_schema


class FoodItemForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Achilles - Food Item")

        self.args = argparse.Namespace(
            debug=False,
            database="achilles",
            databasehost="localhost",
            databaseport=5432,
            databaseuser="bbs",
        )

        self.entries = {}
        self.checkboxes = {}

        schema = ui_schema.ui_schema()
        self._build_form(schema.get("FoodItem", {}))

        button_frame = Frame(root)
        button_frame.pack(fill=X, padx=10, pady=10)

        Button(button_frame, text="Save", command=self._save).pack(side=LEFT, padx=5)
        Button(button_frame, text="Clear", command=self._clear).pack(side=LEFT, padx=5)
        Button(button_frame, text="Load", command=self._load).pack(side=LEFT, padx=5)

    def _build_form(self, schema):
        frame = Frame(self.root)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        row = 0
        for key, meta in schema.items():
            label = Label(frame, text=meta.get("label", key))
            label.grid(row=row, column=0, sticky=W, pady=2)

            if meta.get("type") == "bool":
                var = BooleanVar(value=False)
                cb = Checkbutton(frame, text="", variable=var)
                cb.grid(row=row, column=1, sticky=W, pady=2)
                self.checkboxes[key] = var
            else:
                entry = Entry(frame, width=40)
                entry.grid(row=row, column=1, sticky=W, pady=2)
                self.entries[key] = entry

            row += 1

    def _get_values(self):
        values = {}
        for key, entry in self.entries.items():
            val = entry.get().strip()
            if val:
                values[key] = val
        for key, var in self.checkboxes.items():
            values[key] = var.get()
        return values

    def _set_values(self, values):
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            val = values.get(key, "")
            if val is not None:
                entry.insert(0, str(val))
        for key, var in self.checkboxes.items():
            var.set(bool(values.get(key, False)))

    def _clear(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        for var in self.checkboxes.values():
            var.set(False)

    def _save(self):
        values = self._get_values()
        if not values.get("name"):
            print("ERROR: name is required")
            return

        try:
            with database.connect(self.args) as pool:
                f = libfooditem.FoodItem(self.args, pool=pool)

                for key, val in values.items():
                    if hasattr(f, key):
                        setattr(f, key, val)

                rec = f.buildrec()
                database.insert(
                    self.args,
                    "achilles.__fooditem",
                    rec,
                    primarykey="id",
                    conn=pool,
                    commit=True,
                )
                print(f"Saved: {values.get('name')}")
        except Exception as e:
            print(f"ERROR saving: {e}")

    def _load(self):
        try:
            with database.connect(self.args) as pool:
                f = libfooditem.select(self.args, pool=pool)
                if f is not None:
                    values = {}
                    for key in self.entries.keys():
                        if hasattr(f, key):
                            values[key] = getattr(f, key, None)
                    for key in self.checkboxes.keys():
                        if hasattr(f, key):
                            values[key] = getattr(f, key, False)
                    self._set_values(values)
        except Exception as e:
            print(f"ERROR loading: {e}")


def main():
    root = Tk()
    FoodItemForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()
