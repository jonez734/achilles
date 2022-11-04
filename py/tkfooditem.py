from tkinter import *
from tkinter import ttk

import ttyio5 as ttyio
import bbsengine5 as bbsengine

root = Tk()
root.title("achilles")

frameFoodItem = Frame(root)

fields = {
    "brandid" : {"label": "brand",  "type": "fk"},
    "manufid" : {"label": "manuf",  "type": "fk"},
    "upc":      {"label": "UPC",    "type": "text"},
    "sku":      {"label": "SKU",    "type": "text"},
    "name":     {"label": "name",   "type": "text"},
    "title":    {"label": "title",  "type": "text"},
    "frozen":   {"label": "frozen", "type": "checkbutton"}    
}
entries = {}

r = 0
for key, f in fields.items():
#    Entry(frameFoodItem)
    
    if f["type"] == "checkbutton":
        entry = Checkbutton(frameFoodItem, text=f["label"], font=("Helvetica", 16))
        entry.grid(row=r, column=0, pady=5, sticky=W)
    else:
        label = Label(frameFoodItem, text=f["label"], font=("Helvetica", 16))
        label.grid(row=r, column=0, columnspan=2, pady=10, sticky=W)
        entry = Entry(frameFoodItem)
        entry.grid(row=r, column=2, pady=5, sticky=W)
    entries[key] = entry
    r += 1

frameFoodItem.pack()
root.mainloop()
ttyio.echo(f"entries={entries}", level="debug")
