databaseSchema = '''
BEGIN;

CREATE TABLE IF NOT EXISTS trackslog (
    scrobbleHash TEXT NOT NULL UNIQUE,
    playedOnTime INTEGER NOT NULL UNIQUE,
    artistName   TEXT NOT NULL,
    trackName    TEXT NOT NULL,
    albumName    TEXT DEFAULT NULL,
    PRIMARY KEY(scrobbleHash)
);

CREATE INDEX idx_playedOnTime ON trackslog(playedOnTime);
CREATE INDEX idx_artistName ON trackslog(artistName COLLATE NOCASE);
CREATE INDEX idx_trackName ON trackslog(trackName COLLATE NOCASE);
CREATE INDEX idx_albumName ON trackslog(albumName COLLATE NOCASE);

COMMIT;
'''
