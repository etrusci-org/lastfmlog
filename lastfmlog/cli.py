#!/usr/bin/env python3

import sys

import lastfmlog




def main() -> None:
    print(lastfmlog.banner)
    print()

    CLIParser = lastfmlog.CLIParser(conf=lastfmlog.conf['cliparser'])

    if len(sys.argv) < 2:
        CLIParser.printHelp()
    else:
        args = CLIParser.parseArgs()
        App = lastfmlog.Core(conf=lastfmlog.conf['app'], args=args)

        if args['action'] == 'update':
            App.update()

        if args['action'] == 'stats':
            App.stats()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n! Action aborted by user.')
    finally:
        print()
