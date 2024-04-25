import os, csv, argparse, locale, time

from bbsengine6 import io, database, util, sig
from vulcan import lib as libvulcan

def buildargs(args=None, **kw):
    parser = argparse.ArgumentParser("import csv achilles")

def buildargs(args=None, **kw):
    parser = argparse.ArgumentParser("achillesimportcsv")
    parser.add_argument("--verbose", action="store_true", dest="verbose")
    parser.add_argument("--debug", action="store_true", dest="debug")

    parser.add_argument("filename", nargs="?", default="vulcan-achilles-20230707.csv")

    defaults = {"databasename": "zoid6", "databasehost":"localhost", "databaseuser": None, "databaseport":5432, "databasepassword":None}
    database.buildargdatabasegroup(parser, defaults)
    
    return parser

def buildabsolutefilename(*parts):
    # ~jam/projects/yummy/article2 -> /home/jam/projects...
    # $HOME/projects/yummy/article2 -> /home/jam/...
#    basedir = args.basedir if args.basedir is not None else ""
#    basedir = os.path.expanduser(basedir)
#    basedir = os.path.expandvars(basedir)
    munged = []
    for p in parts:
        q = os.path.normpath(p)
        q = os.path.expanduser(q)
        q = os.path.expandvars(q)
        munged.append(q)
    j = os.path.join(*munged)
    return j

def buildlinkdict(args, row):
#    io.echo(f"buildlinkdict.100: {row=}", level="debug")

    link = {}

    for col in ("url", "title", "description", "postedbymoniker", "dateposted", "lastmodified", "lastmodifiedbymoniker", "broken", "brokenbymoniker", "datebroken", "approved", "approvedbymoniker", "dateapproved"):
        if col in row:
            if col in row and row[col] == "":
                link[col] = None
            else:
                link[col] = row[col]

    sigs = database.postgres_to_python_list(row["sigs"])
    sigs = [s for s in sigs if s]
    if len(sigs) != 1:
        sigs = ""

    link["sigs"] = sigs[0]

    keywords = database.postgres_to_python_list(row["keywords"])
    keywords = [k for k in keywords if k]
    link["keywords"] = keywords

    flags = {}
    if "eros" in row:
        flags["eros"] = row["eros"]
#        del row["eros"]
    if "magic" in row:
        flags["magic"] = row["magic"]
#        del row["magic"]
    link["flags"] = flags
    
    return link

def processrow(args, table, row):
#    io.echo(f"{row=}", level="debug")
    return (buildlinkdict(args, row), [])

def processcsv(args, filename, table, callback=None, **kw):
    # fn = buildabsolutefilename(args.basedir, args.csvdir, filename)
    fn = buildabsolutefilename(filename)
    if args.debug is True:
        io.echo(f"processcsv: {table=} {fn=}")

    rowcount = 0
    csvchanges = []

    with open(fn) as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            (link, changes) = processrow(args, table, row)
            io.echo(f"processcsv.100: {link=}", level="debug")
            rowcount += 1
#            for col in ("id", "sigid", "postedby", "lastmodifiedby", "brokenbyid", "approvedbyid", "datepostedepoch", "dateapprovedepoch", "datebrokenepoch", "age"):
#                if col in rec:
#                    del rec[col]
#                if "postedbyname" in rec:
#                    rec["postedbymoniker"] = rec["postedbyname"]
#                    del rec["postedbyname"]
#                if "approvedbyname" in rec:
#                    rec["approvedbymoniker"] = rec["approvedbyname"]
#                    del rec["approvedbyname"]

#                io.echo(f"{rec=}", level="debug")

                # database.insert(args, table, rec, returnid=False, mogrify=True)
            if sig.exists(args, link["sigs"][0]) is False:
                s = {}
                s["path"] = link["sigs"]
                s["uri"] = ""
                s["title"] = f"the {link['sigs']} sig"
                s["intro"] = ""
                s["attributes"] = {} # database.Json({})
                # io.echo(f"{s=}", level="debug")
                
                if sig.exists(args, s["path"]) is False:
                    sig.insert(args, s)
                    io.echo(f"{s=} added", level="debug")
                else:
                    io.echo(f"{s['path']=} exists", level="debug")
            url = link["url"]
            if libvulcan.linkexists(args, url) is False:
                libvulcan.insertlink(args, link)
                libvulcan.setsigs(args, url, link["sigs"])
            else:
                io.echo(f"{url=} exists", level="debug")
        database.commit(args)
    for c in csvchanges:
        io.echo(c)

    io.echo(f"{os.path.basename(csvfile.name)} {util.pluralize(rowcount, 'row', 'rows')}")
#    database.commit(args)

def main(args, **kw):
    util.heading("import achilles csv file")
    dbh = database.connect(args)
    processcsv(args, args.filename, "vulcan.__link")
    database.commit(args)

if __name__ == "__main__":
    parser = buildargs()
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, "")
    time.tzset()

#    init(args)

    try:
        main(args)
    except KeyboardInterrupt:
        io.echo("{/all}{bold}INTR{bold}")
    except EOFError:
        io.echo("{/all}{bold}EOF{/bold}")
    finally:
        io.echo("{decsc}{curpos:%d,0}{el}{decrc}{reset}{/all}" % (io.getterminalheight()))
    