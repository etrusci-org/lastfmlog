# Database schema (transaction)
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

    CREATE INDEX indexPlayTime ON trackslog(playTime DESC);
    CREATE INDEX indexArtist ON trackslog(artist COLLATE NOCASE ASC);
    CREATE INDEX indexTrack ON trackslog(track COLLATE NOCASE ASC);
    CREATE INDEX indexAlbum ON trackslog(album COLLATE NOCASE ASC);

    COMMIT;
'''
