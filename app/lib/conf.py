import os




conf = {}

conf['libDir'] = os.path.dirname(__file__)

conf['defaultDataDir'] = os.path.abspath(os.path.join(conf['libDir'], '..', 'data'))

conf['secretsFileName'] = 'secrets.json'

conf['statsFileName'] = 'stats.json'

conf['dbFileName'] = 'main.sqlite3'

conf['dbSchema'] = '''
    BEGIN;
    CREATE TABLE IF NOT EXISTS trackslog (
        scrobbleHash TEXT NOT NULL UNIQUE,
        playedOnTime INTEGER NOT NULL UNIQUE,
        artistName   TEXT NOT NULL,
        trackName    TEXT NOT NULL,
        albumName    TEXT DEFAULT NULL,
        PRIMARY KEY(scrobbleHash)
    );
    CREATE INDEX idx_playedOnTime ON trackslog(playedOnTime DESC);
    CREATE INDEX idx_artistName ON trackslog(artistName COLLATE NOCASE ASC);
    CREATE INDEX idx_trackName ON trackslog(trackName COLLATE NOCASE ASC);
    CREATE INDEX idx_albumName ON trackslog(albumName COLLATE NOCASE ASC);
    COMMIT;
'''

conf['api'] = {
    'baseURL': 'http://ws.audioscrobbler.com/2.0/',
    'itemsPerPageLimitInitial': 200,
    'itemsPerPageLimitIncremental': 20,
    'subsequentPageRequestDelay': 10,
}

conf['argDefaults'] = {
    'datadir': conf['defaultDataDir'],
    'obsoleteafter': 1800,
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
            'help': 'Do something.',
        },
        {
            'arg': ['-d', '--datadir'],
            'metavar': 'PATH',
            'type': str,
            'required': False,
            'default': conf['argDefaults']['datadir'],
            'help': 'Override default data directory path.',
        },
        # options when action=update
        {
            'arg': '--updatefromstart',
            'action': 'store_true',
            'help': '[update] Fetch tracks from the beginning of time.',
        },
        # options when action=stats
        {
            'arg': ['-o', '--obsoleteafter'],
            'metavar': 'SECONDS',
            'type': int,
            'required': False,
            'default': conf['argDefaults']['obsoleteafter'],
            'help': '[stats] Time in seconds until the database is considered obsolete. Set to -1 to disable this check.',
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

conf['banner'] = ''' _            _    __       _
| |   __ _ __| |_ / _|_ __ | |   ___  __ _
| |__/ _` (_-<  _|  _| '  \| |__/ _ \/ _` |
|____\__,_/__/\__|_| |_|_|_|____\___/\__, |
                                     |___/
'''
