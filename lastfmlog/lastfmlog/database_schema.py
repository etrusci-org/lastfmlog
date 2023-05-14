databaseSchema = [
    '''
        CREATE TABLE IF NOT EXISTS trackslog (
            scrobbleHash TEXT NOT NULL UNIQUE,
            playedOnTime INTEGER NOT NULL UNIQUE,
            artistName   TEXT NOT NULL,
            trackName    TEXT NOT NULL,
            albumName    TEXT,
            PRIMARY KEY(scrobbleHash)
        );
    ''',
]
