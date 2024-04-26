import time, locale

from bbsengine6 import io, session, screen

from . import lib

def init(args, **kw):
    return True

def access(args, op, **kw):
    return True

if __name__ == "__main__":
    parser = lib.buildargs()
    args = parser.parse_args()

    session.start(args)

    screen.init()
    init(args)

    locale.setlocale(locale.LC_ALL, "")
    time.tzset()

    try:
        lib.runmodule(args, "main") # main(args) # lib.runsubmodule(args, "main") # module.main(args)
    except KeyboardInterrupt:
        io.echo("{/all}*INTR*")
    except EOFError:
        io.echo("{/all}*EOF*")
    finally:
        io.echo("{decsc}{curpos:%d,0}{el}{decrc}{reset}{/all}" % (io.getterminalheight()))
