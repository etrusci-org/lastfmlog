#!/usr/bin/env python3

import sys
import time

import lastfmloglib




# Init logger
Log = lastfmloglib.log.Logger()

# Init command line argument parser
CLIParser = lastfmloglib.CLIParser(conf=lastfmloglib.conf['cliparser'])




def main() -> None:
    # Print help and stop if the user has not provided any arguments
    if len(sys.argv) < 2:
        CLIParser.printHelp()
        return

    # We got command line arguments if we reach this line, parse them
    cliargs = CLIParser.parseArgs()

    # Init the app
    App = lastfmloglib.App(conf=lastfmloglib.conf, args=cliargs, Log=Log)

    # Run actions
    startTime = time.time()

    if not cliargs['json']:
        msg = f'/ L a s t f m L o g  {cliargs["action"]}'
        Log.msg(msg)
        Log.msg(''.rjust(len(msg), '-'))
        Log.msg()

    App.executeAction(action=cliargs['action'])

    if not cliargs['json']:
        msg = f'\ {round(time.time() - startTime, 4)}s'
        Log.msg()
        Log.msg(''.ljust(len(msg), '-'))
        Log.msg(msg)




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Log.msg('\nprogram interrupted by user')
    except Exception as e:
        Log.msg(f'[BOO] {e}', end='\n\n')
        Log.msg('complete error log:')
        raise
