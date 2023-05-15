#!/usr/bin/env python3

import sys

import lastfmlog




def main() -> None:
    print(lastfmlog.banner)

    CLIParser = lastfmlog.CLIParser(conf=lastfmlog.conf['cliparser'])

    if len(sys.argv) < 2:
        CLIParser.printHelp()
        return

    args = CLIParser.parseArgs()
    App = lastfmlog.App(conf=lastfmlog.conf['app'], args=args)

    print(f'# Action: {args["action"]}')

    if args['action'] == 'update':
        App.update()

    if args['action'] == 'stats':
        App.stats()

    print('# Done')




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n! Action aborted by user.')
