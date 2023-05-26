#!/usr/bin/env python3

import sys

import lastfmloglib




def main():
    # Init command line argument parser
    CLIParser = lastfmloglib.CLIParser(conf=lastfmloglib.conf['cliparser'])

    # Print help and stop if the user has not provided any arguments
    if len(sys.argv) < 2:
        CLIParser.printHelp()
        return

    # We got command line arguments if we reach this line, parse them
    cliargs = CLIParser.parseArgs()

    # Init the app
    App = lastfmloglib.App(conf=lastfmloglib.conf, args=cliargs)

    # Run actions
    if not cliargs['json']:
        print(f'[lastfmlog {cliargs["action"]}]', end='\n\n')

    if cliargs['action'] == 'whoami':
        App.whoami()

    if cliargs['action'] == 'update':
        App.update()

    if cliargs['action'] == 'stats':
        App.stats()

    if cliargs['action'] == 'nowplaying':
        App.nowplaying()

    if cliargs['action'] == 'resetdatabase':
        App.resetDatabase()

    if cliargs['action'] == 'resetsecrets':
        App.resetSecrets()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram interrupted by user.')
    except Exception as e:
        print(f'[BOO] {e}', end='\n\n')
        print('Complete error log:')
        raise
