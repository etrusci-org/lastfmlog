databaseSchema = '''
    BEGIN;


    CREATE TABLE IF NOT EXISTS trackslog (
        playHash TEXT NOT NULL UNIQUE,
        playTime INTEGER NOT NULL UNIQUE,
        artist TEXT NOT NULL,
        track TEXT NOT NULL,
        album TEXT DEFAULT NULL,
        PRIMARY KEY(playHash)
    );


    CREATE INDEX idx_playTime ON trackslog(playTime DESC);
    CREATE INDEX idx_artist ON trackslog(artist COLLATE NOCASE ASC);
    CREATE INDEX idx_track ON trackslog(track COLLATE NOCASE ASC);
    CREATE INDEX idx_album ON trackslog(album COLLATE NOCASE ASC);


    COMMIT;
'''
