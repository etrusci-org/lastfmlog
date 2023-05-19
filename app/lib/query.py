query = {}

query['dbSchema'] = '''
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

query['insertNewTrack'] = '''
INSERT INTO
    trackslog (
        scrobbleHash,
        playedOnTime,
        artistName,
        trackName,
        albumName
    )
VALUES (
    :scrobbleHash,
    :playedOnTime,
    :artistName,
    :trackName,
    :albumName
);
'''

query['trackslogRowCount'] = '''
SELECT
    COUNT(scrobbleHash) AS playcount
FROM
    trackslog;
'''

query['playsByYear'] = '''
SELECT
    strftime('%Y', playedOnTime, 'unixepoch') AS year,
    COUNT(scrobbleHash) AS playcount
FROM trackslog
GROUP BY
    year
ORDER BY
    year DESC
LIMIT
    :limit;
'''

query['playsByMonth'] = '''
SELECT
    strftime('%Y-%m', playedOnTime, 'unixepoch') AS month,
    COUNT(scrobbleHash) AS playcount
FROM
    trackslog
GROUP BY
    month
ORDER BY
    month DESC
LIMIT
    :limit;
'''

query['playsByDay'] = '''
SELECT
    strftime('%Y-%m-%d', playedOnTime, 'unixepoch') AS day,
    COUNT(scrobbleHash) AS playcount
FROM
    trackslog
GROUP BY
    day
ORDER BY
    day DESC
LIMIT
    :limit;
'''

query['playsByHour'] = '''
SELECT
    strftime('%Y-%m-%d %H', playedOnTime, 'unixepoch') AS hour,
    COUNT(scrobbleHash) AS playcount
FROM
    trackslog
GROUP BY
    hour
ORDER BY
    hour DESC
LIMIT
    :limit;
'''

query['uniqueArtists'] = '''
SELECT
    COUNT(DISTINCT artistName COLLATE NOCASE) AS playcount
FROM
    trackslog;
'''

query['uniqueTracks'] = '''
SELECT
    COUNT(DISTINCT artistName || trackName COLLATE NOCASE) AS playcount
FROM
    trackslog;
'''

query['uniqueAlbums'] = '''
SELECT
    COUNT(DISTINCT artistName || albumName COLLATE NOCASE) AS playcount
FROM
    trackslog;
'''

query['topArtists'] = '''
SELECT
    artistName,
    COUNT(artistName) AS playcount
FROM
    trackslog
GROUP BY
    artistName COLLATE NOCASE
ORDER BY
    playcount DESC
LIMIT :limit;
'''

query['topTracks'] = '''
SELECT
    artistName,
    trackName,
    COUNT(artistName || trackName COLLATE NOCASE) AS playcount
FROM
    trackslog
GROUP BY
    (artistName || trackName COLLATE NOCASE)
ORDER BY
    playcount DESC
LIMIT
    :limit;
'''

query['topAlbums'] = '''
SELECT
    CASE
        WHEN COUNT(DISTINCT artistName) > 1
        THEN 'Various Artists'
        ELSE MAX(artistName)
    END AS artistName,
    albumName,
    COUNT(albumName) AS playcount
FROM
    trackslog
WHERE
    albumName IS NOT NULL
GROUP BY
    albumName COLLATE NOCASE
ORDER BY
    playcount DESC
LIMIT
    :limit;
'''
