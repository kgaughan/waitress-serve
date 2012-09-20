import getopt
import re
import sys

import waitress


RUNNER_PATTERN = re.compile("""
    ^
    (?P<module>
        [a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)*
    )
    :
    (?P<object>
        [a-z_][a-z0-9_]*
    )
    $
    """, re.I | re.X)


def parse_opts(argv, opt_map):
    long_opts = []
    for opt, cast in opt_map.iteritems():
        if cast is bool:
            long_opts.append(opt)
        else:
            long_opts.append(opt + '=')
    opts, args = getopt.getopt(argv, '', long_opts)
    kwargs = {}
    for opt, arg in opts:
        opt = opt.lstrip('-')
        if opt not in opt_map:
            print >> sys.stderr, "Invalid option: %s" % opt
            sys.exit(1)
        arg = opt_map[opt](arg)
        if opt.startswith('no-'):
            opt = opt[5:]
            arg = not arg
        kwargs[opt.replace('-', '_')] = arg
    return kwargs, args


def main():
    opt_map = {
        'host': str,
        'port': int,
        'threads': int,
        'url-scheme': str,
        'ident': str,
        'backlog': int,
        'recv-bytes': int,
        'send-bytes': int,
        'outbuf-overflow': int,
        'inbuf-overflow': int,
        'connection-limit': int,
        'cleanup-interval': int,
        'channel-timeout': int,
        'no-log-socket-errors': bool,
        'max-request-header-size': int,
        'max-request-body-size': int,
        'expose-tracebacks': bool
    }
    kwargs, args = parse_opts(sys.argv[1:], opt_map)
    if len(args) != 1:
        print >> sys.stderr, 'Please specify one and only one application'
        return 1
    matches = RUNNER_PATTERN.match(args[0])
    if not matches:
        print >> sys.stderr, "Malformed application: '%s'" % args[0]
        return 1

    module_name = matches.group('module')
    object_name = matches.group('object')

    module = __import__(module_name, globals(), locals(), [object_name], -1)
    app = getattr(module, object_name)
    waitress.serve(app, **kwargs)
    return 0


if __name__ == '__main__':
    sys.exit(main())