from bbsengine6 import io

from . import lib

def init(args, **kw:dict) -> bool:
    return True

def access(args, op:str, **kw:dict) -> bool:
    return True

def buildargs(args, **kw:dict) -> bool:
    return None

def main(args, **kw):
  fooditem = {}
  fooditem["upc"] = None
  fooditem["sku"] = None
  fooditem["lot"] = None
  fooditem["serial"] = None
  fooditem["name"] = None
  fooditem["title"] = None
  fooditem["description"] = None
  fooditem["frozen"] = True
  fooditem["wic"] = True

  _fooditem = lib._edit(args, fooditem, "add")

  if fooditem != _fooditem:
    io.echo("** needs save **", level="info")
  if io.inputboolean(f"{{promptcolor}}add fooditem? {{optioncolor}}[yN]{{promptcolor}}: {{inputcolor}}", "N") is True:
    io.echo("...code to add fooditem...")
  return
