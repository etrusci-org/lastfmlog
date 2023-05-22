import os




conf = {}


conf['dataDir'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))


conf['secretsTemplate'] = {
    'apiUser': 'YOUR_LASTFM_API_USERNAME_HERE',
    'apiKey': 'YOUR_LASTFM_API_KEY_HERE'
}


conf['apiBaseURL'] = 'https://ws.audioscrobbler.com/2.0/'
conf['apiRequestLimitInitial'] = 200
conf['apiRequestLimitIncremental'] = 30
conf['apiRequestSwitchToInitialLimitTreshold'] = 86400
conf['apiRequestPagingDelay'] = 7


conf['cliparserActions'] = [
    'whoami',
    'update',
    'stats',
    'reset',
]

conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'For more detailed explanations, please see the README.',
        'epilog': '',
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
            'arg': ['-v', '--verbose'],
            'action': 'store_true',
            'required': False,
            'help': f'Show more output while actions are executed.',
        },
        {
            'arg': '--datadir',
            'metavar': 'PATH',
            'type': str,
            'required': False,
            'default': None,
            'help': f'Override default data directory path.',
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
    ]
}
