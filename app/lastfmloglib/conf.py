import os

from .argtypes import cliparserArgTypeQueryLimit
from .argtypes import cliparserArgTypeFrom
from .argtypes import cliparserArgTypeTo
from .argtypes import cliparserArgTypeExistingDirectoryPath




conf = {}


# Default data directory path
conf['dataDir'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Secrets filename (binary)
conf['secretsFilename'] = 'secrets.bin'

# Database filename (sqlite3)
conf['databaseFilename'] = 'database.sqlite3'

# Stats filename (json)
conf['statsFilename'] = 'stats.json'

# Database dump filename (sql)
conf['exportFilename'] = 'export.sql'

# API base URL with trailing slash
conf['apiBaseURL'] = 'https://ws.audioscrobbler.com/2.0/'

# Number of items per page to request when database is empty or outdated
conf['apiRequestLimitInitial'] = 200

# Number of items per page to request when database not empty and not outdated
conf['apiRequestLimitIncremental'] = 20

# Time in seconds until the database is considered outdated
conf['apiRequestSwitchToInitialLimitTreshold'] = 86400 / 2 # seconds

# Time in seconds before requesting the next page if it is a paged result
conf['apiRequestPagingDelay'] = 7

# Actions the user can run
conf['actionArgs'] = [
    'testsecrets',
    'nowplaying',
    'update',
    'stats',
    'export',
    'trimdatabase',
    'resetdatabase',
    'resetsecrets',
]

# Command line parser config and arguments
# These are also the defaults
conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'for more detailed explanations, please see the README <https://github.com/etrusci-org/lastfmlog#readme>',
        'epilog': 'made by arT2 <etrusci.org>',
    },
    'args': [
        {
            'arg': 'action',
            'metavar': 'ACTION',
            'type': str,
            'choices': conf['actionArgs'],
            'help': f'run an action, choose from: {", ".join(conf["actionArgs"])}',
        },
        # global options
        {
            'arg': '--datadir',
            'metavar': 'PATH',
            'type': cliparserArgTypeExistingDirectoryPath,
            'required': False,
            'default': None,
            'help': f'override default data directory path',
        },
        # update options
        {
            'arg': '--from',
            'metavar': 'UNIXTIME',
            'type': cliparserArgTypeFrom,
            'required': False,
            'default': None,
            'help': '[update] only fetch plays after this time',
        },
        {
            'arg': '--to',
            'metavar': 'UNIXTIME',
            'type': cliparserArgTypeTo,
            'required': False,
            'default': None,
            'help': '[update] only fetch plays before this time',
        },
        # stats options
        {
            'arg': '--limitall',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in all lists',
        },
        {
            'arg': '--limittopartists',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in top artists',
        },
        {
            'arg': '--limittoptracks',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in top tracks',
        },
        {
            'arg': '--limittopalbums',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in top albums',
        },
        {
            'arg': '--limitplaysbyyear',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in plays by year',
        },
        {
            'arg': '--limitplaysbymonth',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in plays by month',
        },
        {
            'arg': '--limitplaysbyday',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in plays by day',
        },
        {
            'arg': '--limitplaysbyhour',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] limit the number of items in plays by hour',
        },
    ]
}
