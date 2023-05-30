import os

from .argtypes import cliparserArgTypeQueryLimit
from .argtypes import cliparserArgTypeFrom
from .argtypes import cliparserArgTypeTo
from .argtypes import cliparserArgTypeExistingDirectoryPath




conf = {}


conf['dataDir'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
conf['secretsFilename'] = 'secrets.bin'
conf['databaseFilename'] = 'database.sqlite3'
conf['statsFilename'] = 'stats.json'
conf['exportFilename'] = 'export.sql'


conf['apiBaseURL'] = 'https://ws.audioscrobbler.com/2.0/'
conf['apiRequestLimitInitial'] = 200
conf['apiRequestLimitIncremental'] = 20
conf['apiRequestSwitchToInitialLimitTreshold'] = 86400 / 2
conf['apiRequestPagingDelay'] = 7


conf['actionArgs'] = [
    'whoami',
    'nowplaying',
    'update',
    'stats',
    'export',
    'trimdatabase',
    'resetdatabase',
    'resetsecrets',
]


conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'For more detailed explanations, please see the README <https://github.com/etrusci-org/lastfmlog#readme>.',
        'epilog': 'Made by arT2 <etrusci.org>',
    },
    # TODO: update help texts
    'args': [
        {
            'arg': 'action',
            'metavar': 'ACTION',
            'type': str,
            'choices': conf['actionArgs'],
            'help': f'Run an action. Choose from: {", ".join(conf["actionArgs"])}',
        },
        # global options
        {
            'arg': '--datadir',
            'metavar': 'PATH',
            'type': cliparserArgTypeExistingDirectoryPath,
            'required': False,
            'default': None,
            'help': f'Override default data directory path.',
        },
        # nowplaying options
        {
            'arg': '--json',
            'action': 'store_true',
            'required': False,
            'help': f'[nowplaying] Show JSON instead of plain text output.',
        },
        # update options
        {
            'arg': '--from',
            'metavar': 'UNIXTIME',
            'type': cliparserArgTypeFrom,
            'required': False,
            'default': None,
            'help': '[update] Only fetch plays after this time.',
        },
        {
            'arg': '--to',
            'metavar': 'UNIXTIME',
            'type': cliparserArgTypeTo,
            'required': False,
            'default': None,
            'help': '[update] Only fetch plays before this time.',
        },
        # stats options
        {
            'arg': '--limittopartists',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top artists.',
        },
        {
            'arg': '--limittoptracks',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top tracks.',
        },
        {
            'arg': '--limittopalbums',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top albums.',
        },
        {
            'arg': '--limitplaysbyyear',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by year.',
        },
        {
            'arg': '--limitplaysbymonth',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by month.',
        },
        {
            'arg': '--limitplaysbyday',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by day.',
        },
        {
            'arg': '--limitplaysbyhour',
            'metavar': 'NUMBER',
            'type': cliparserArgTypeQueryLimit,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by hour.',
        },
    ]
}
