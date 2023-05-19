import os




conf = {}

conf['libDir'] = os.path.dirname(__file__)

conf['defaultDataDir'] = os.path.abspath(os.path.join(conf['libDir'], '..', 'data'))

conf['secretsFileName'] = 'secrets.json'

conf['statsFileName'] = 'stats.json'

conf['dbFileName'] = 'main.sqlite3'

conf['api'] = {
    'baseURL': 'http://ws.audioscrobbler.com/2.0/',
    'itemsPerPageLimitInitial': 200,
    'itemsPerPageLimitIncremental': 20,
    'subsequentPageRequestDelay': 10,
}

conf['argDefaults'] = {
    'datadir': conf['defaultDataDir'],
    'obsoleteafter': 1800,
    'from': -1,
    'to': -1,
}

conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'Check README for more detailed help.',
        'epilog': f'Made with <3 by arT2 <etrusci.org>',
    },
    'args': [
        {
            'arg': 'action',
            'metavar': 'ACTION',
            'type': str,
            'choices': ['update', 'stats', 'reset'],
            'help': 'Do something. Choose from action, stats or update.',
        },
        {
            'arg': '--datadir',
            'metavar': 'PATH',
            'type': str,
            'required': False,
            'default': conf['argDefaults']['datadir'],
            'help': f'Override default data directory path. Default: {conf["argDefaults"]["datadir"]}',
        },
        # options when action=update
        {
            'arg': '--from',
            'metavar': 'UNIXTIME',
            'type': int,
            'required': False,
            'default': conf['argDefaults']['from'],
            'help': f'[update] Only fetch plays after this time. Default: incremental update',
        },
        {
            'arg': '--to',
            'metavar': 'UNIXTIME',
            'type': int,
            'required': False,
            'default': conf['argDefaults']['to'],
            'help': f'[update] Only fetch plays before this time. Default: incremental update',
        },
        # options when action=stats
        {
            'arg': '--obsoleteafter',
            'metavar': 'SECONDS',
            'type': int,
            'required': False,
            'default': conf['argDefaults']['obsoleteafter'],
            'help': f'[stats] Set the time in seconds until the database is considered obsolete, and you will be asked if you want to update it first. Set to -1 to disable this check. Default: {conf["argDefaults"]["obsoleteafter"]}',
        },
        {
            'arg': '--playsbyyearlimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by year.',
        },
        {
            'arg': '--playsbymonthlimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by month.',
        },
        {
            'arg': '--playsbydaylimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by day.',
        },
        {
            'arg': '--playsbyhourlimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in plays by hour.',
        },
        {
            'arg': '--topartistslimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top artists.',
        },
        {
            'arg': '--toptrackslimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top tracks.',
        },
        {
            'arg': '--topalbumslimit',
            'metavar': 'NUMBER',
            'type': int,
            'required': False,
            'default': None,
            'help': '[stats] Limit the number of items in top albums.',
        },
    ],
}
