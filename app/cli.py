#!/usr/bin/env python3

import sys

import lib




def main() -> None:
    print(lib.conf['banner'])

    CLIParser = lib.CLIParser(conf=lib.conf['cliparser'])

    if len(sys.argv) < 2:
        CLIParser.printHelp()
        return

    cliargs = CLIParser.parseArgs()

    App = lib.Core(conf=lib.conf, args=cliargs)

    if cliargs['action'] == 'update':
        App.update()

    if cliargs['action'] == 'stats':
        App.stats()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nAction stopped manually the user')
