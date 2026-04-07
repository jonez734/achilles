import time
import locale

from bbsengine6 import database, io, screen, session

from . import lib


def init(args, **kw):
    return None


def access(args, op, **kw):
    return None


if __name__ == "__main__":
    parser = lib.buildargs()
    args = parser.parse_args()

    screen.init()
    init(args)

    locale.setlocale(locale.LC_ALL, "")
    time.tzset()

    with database.getpool(args, dbname=args.databasename) as pool:
        if session.start(args, pool=pool) is False:
            io.echo("achilles.__main__: session.start() failed", level="error")
        else:
            try:
                lib.runmodule(args, "main")
            except KeyboardInterrupt:
                io.echo("{/all}*INTR*")
            except EOFError:
                io.echo("{/all}*EOF*")
            finally:
                io.echo(
                    f"{{savecursor}}{{curpos:{io.terminal.height()},0}}{{el}}{{reset}}{{restorecursor}}"
                )
