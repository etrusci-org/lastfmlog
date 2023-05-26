import os




conf = {}


conf['dataDir'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))


conf['apiBaseURL'] = 'https://ws.audioscrobbler.com/2.0/'
conf['apiRequestLimitInitial'] = 200
conf['apiRequestLimitIncremental'] = 30
conf['apiRequestSwitchToInitialLimitTreshold'] = 86400
conf['apiRequestPagingDelay'] = 7


conf['cliparserActions'] = [
    'whoami',
    'nowplaying',
    'update',
    'stats',
    'resetdatabase',
    'resetsecrets',
]


conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'For more detailed explanations, please see the README <https://github.com/etrusci-org/lastfmlog#readme>.',
        'epilog': 'Made by arT2 <etrusci.org>',
    },
    'args': [
        {
            'arg': 'action',
            'metavar': 'ACTION',
            'type': str,
            'choices': conf['cliparserActions'],
            'help': f'Execute an action. Choose from: {", ".join(conf["cliparserActions"])}',
        },
        # global options
        {
            'arg': '--datadir',
            'metavar': 'PATH',
            'type': str,
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
            'type': int,
            'required': False,
            'default': None,
            'help': '[update] Only fetch plays after this time.',
        },
        {
            'arg': '--to',
            'metavar': 'UNIXTIME',
            'type': int,
            'required': False,
            'default': None,
            'help': '[update] Only fetch plays before this time.',
        },
        {
            'arg': ['-v', '--verbose'],
            'action': 'store_true',
            'required': False,
            'help': f'[update] Show fetched tracks while updating.',
        },
        # stats options
        {
            'arg': '--limittopartists',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top artists.',
        },
        {
            'arg': '--limittoptracks',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top tracks.',
        },
        {
            'arg': '--limittopalbums',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top albums.',
        },
        {
            'arg': '--limitplaysbyyear',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by year.',
        },
        {
            'arg': '--limitplaysbymonth',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by month.',
        },
        {
            'arg': '--limitplaysbyday',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by day.',
        },
        {
            'arg': '--limitplaysbyhour',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by hour.',
        },
    ]
}
