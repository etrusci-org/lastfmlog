import os




conf = {}

conf['libDir'] = os.path.dirname(__file__)

conf['defaultDataDir'] = os.path.abspath(os.path.join(conf['libDir'], '..', 'data'))

conf['secretsFileName'] = 'secrets.json'

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

conf['cliparser'] = {
    'info': {
        'prog': 'cli.py',
        'description': 'Check README for more detailed help.',
        'epilog': f'Default data directory: {conf["defaultDataDir"]}',
    },
    'args': [
        {
            'arg': 'action',
            'metavar': 'ACTION',
            'type': str,
            'choices': ['update'],
            'help': 'Do something.',
        },
        {
            'arg': '--updatefromstart',
            'action': 'store_true',
            'help': 'If action is update, fetch tracks from the beginning of time.',
        },
        {
            'arg': ['-d', '--datadir'],
            'metavar': 'PATH',
            'type': str,
            'required': False,
            'default': conf['defaultDataDir'],
            'help': 'Override default data directory path.',
        },
    ],
}

conf['banner'] = ''' _            _    __       _
| |   __ _ __| |_ / _|_ __ | |   ___  __ _
| |__/ _` (_-<  _|  _| '  \| |__/ _ \/ _` |
|____\__,_/__/\__|_| |_|_|_|____\___/\__, |
                                     |___/
'''
