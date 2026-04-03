import os
import csv
import argparse
import locale
import time

from bbsengine6 import io, database, util, sig
from vulcan import lib as libvulcan
# from teos import lib as libteos


def buildargs(args=None, **kw):
    parser = argparse.ArgumentParser("achillesimportcsv")
    parser.add_argument("--verbose", action="store_true", dest="verbose")
    parser.add_argument("--debug", action="store_true", dest="debug")

    parser.add_argument("--dryrun", action="store_true", dest="dryrun")

    parser.add_argument("filename", nargs="?", default="vulcan-achilles-20230707.csv")

    defaults = {
        "databasename": "zoid6",
        "databasehost": "localhost",
        "databaseuser": None,
        "databaseport": 5432,
        "databasepassword": None,
    }
    database.buildargs(parser, defaults)

    return parser


def arraytolist(args, buf):
    return list(buf) if buf is not None else []


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
    link = {}

    for col in (
        "url",
        "title",
        "description",
        "postedbymoniker",
        "dateposted",
        "lastmodified",
        "lastmodifiedbymoniker",
        "broken",
        "brokenbymoniker",
        "datebroken",
        "approved",
        "approvedbymoniker",
        "dateapproved",
    ):
        if col in row:
            if col == "dateposted":
                link["datecreated"] = row[col]
            elif col == "postedbymoniker":
                link["createdbymoniker"] = member.getcurrentmoniker(args)
            elif col in ("datebroken", "brokenbymoniker"):
                continue
            elif col in ("approvedbymoniker", "dateapproved"):
                continue
            elif col in row and row[col] == "":
                link[col] = None
            else:
                link[col] = row[col]

    sigs = [
        "top.achilles",
    ]  # database.postgres_to_python_list(row["sigs"])
    sigs = [s for s in sigs if s]
    if len(sigs) != 1:
        sigs = ""

    link["sigs"] = sigs
    return link


# def processrow(args, table, row):
##    io.echo(f"{row=}", level="debug")
#    return (buildlinkdict(args, row), [])


def processcsv(args, filename, table, callback=None, **kw):
    # fn = buildabsolutefilename(args.basedir, args.csvdir, filename)
    fn = buildabsolutefilename(filename)
    if args.debug is True:
        io.echo(f"processcsv: {table=} {fn=}")

    rowcount = 0

    with open(fn, "r") as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        with database.connect(args) as conn:
            with database.cursor(conn) as cur:
                for row in reader:
                    link = buildlinkdict(args, table, row)
                    if args.debug is True:
                        io.echo(f"processcsv.100: {link=}", level="debug")
                    rowcount += 1

                    url = link["url"]
                    if libvulcan.exists(args, url) is True:
                        io.echo(f"{{gray}}{url=} exists")
                    else:
                        libvulcan.insert(args, link)
                        io.echo(f"{{green}}{url=} added")
                    #                    if link["broken"] is True:
                    #                        libvulcan.setflag(args, url, "broken", True, cur=cur)

                    io.echo(f"{link['sigs']=}", level="debug")
                    #                    sys.exit(-1)

                    sigpath = link["sigs"]

                    io.echo(f"checking for {sigpath=} {type(sigpath)=}", level="debug")

                    if type(sigpath) is str:
                        if sig.exists(args, sigpath, cur=cur) is False:
                            _sig = {}
                            _sig["path"] = sigpath
                            _sig["title"] = f"{sig.striptop(sigpath)}"

                            if sig.insert(args, _sig, cur=cur) is None:
                                io.echo(f"error inserting sig {_sig=}", level="error")
                                break
                        if (
                            libvulcan.setsigs(args, url, sigpath, cur=cur, mogrify=True)
                            is False
                        ):
                            io.echo("error setting sigs for {url} to {sigpath}{/all}")
                            break
                    elif type(sigpath) is list:
                        for s in sigpath:
                            if sig.exists(args, s, cur=cur) is False:
                                _sig = {}
                                _sig["path"] = s
                                _sig["title"] = f"{sig.striptop(s)}"
                                if sig.insert(args, _sig, cur=cur) is None:
                                    io.echo(
                                        f"error inserting sig {_sig=}", level="error"
                                    )
                                    break
                            if libvulcan.setsigs(args, url, s, cur=cur) is False:
                                io.echo(
                                    f"{{labelcolor}}error setting sigs for {{valuecolor}}{url}{{labelcolor}} to {{valuecolor}}{s}"
                                )
                                break
                    else:
                        io.echo(f"{type(sigpath)=} invalid", level="error")
                        break


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
        io.echo(
            "{decsc}{curpos:%d,0}{el}{decrc}{reset}{/all}" % (io.getterminalheight())
        )
