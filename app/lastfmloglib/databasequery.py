databaseQuery = {}

databaseQuery['trackslogInsertNewTrack'] = '''
INSERT INTO trackslog (
    playHash,
    playTime,
    artist,
    track,
    album
)
VALUES (
    :playHash,
    :playTime,
    :artist,
    :track,
    :album
);
'''


databaseQuery['resetDatabase'] = '''
BEGIN;
DELETE FROM trackslog;
COMMIT;
'''


databaseQuery['totalPlays'] = '''
SELECT COUNT(playHash)
FROM trackslog;
'''


databaseQuery['uniqueArtists'] = '''
SELECT COUNT(DISTINCT artist COLLATE NOCASE)
FROM trackslog;
'''


databaseQuery['uniqueTracks'] = '''
SELECT COUNT(DISTINCT artist || track COLLATE NOCASE)
FROM trackslog;
'''


databaseQuery['uniqueAlbums'] = '''
SELECT COUNT(DISTINCT artist || album COLLATE NOCASE)
FROM trackslog;
'''


databaseQuery['topArtists'] = '''
SELECT artist, COUNT(artist) AS plays
FROM trackslog
GROUP BY artist COLLATE NOCASE
ORDER BY plays DESC
LIMIT :limit;
'''


databaseQuery['topTracks'] = '''
SELECT artist, track, COUNT(artist || track COLLATE NOCASE) AS plays
FROM trackslog GROUP BY (artist || track COLLATE NOCASE)
ORDER BY plays DESC
LIMIT :limit;
'''


databaseQuery['topAlbums'] = '''
SELECT CASE WHEN COUNT(DISTINCT artist) > 1 THEN 'Various Artists' ELSE MAX(artist) END AS artist, album, COUNT(album) AS plays
FROM trackslog
WHERE album IS NOT NULL
GROUP BY album COLLATE NOCASE
ORDER BY plays DESC
LIMIT :limit;
'''


databaseQuery['playsByYear'] = '''
SELECT strftime('%Y', playTime, 'unixepoch') AS year, COUNT(playHash) AS plays
FROM trackslog
GROUP BY year
ORDER BY year DESC
LIMIT :limit;
'''


databaseQuery['playsByMonth'] = '''
SELECT strftime('%Y-%m', playTime, 'unixepoch') AS month, COUNT(playHash) AS plays
FROM trackslog
GROUP BY month
ORDER BY month DESC
LIMIT :limit;
'''


databaseQuery['playsByDay'] = '''
SELECT strftime('%Y-%m-%d', playTime, 'unixepoch') AS day, COUNT(playHash) AS plays
FROM trackslog
GROUP BY day
ORDER BY day DESC
LIMIT :limit;
'''


databaseQuery['playsByHour'] = '''
SELECT strftime('%Y-%m-%d %H', playTime, 'unixepoch') AS hour, COUNT(playHash) AS plays
FROM trackslog
GROUP BY hour
ORDER BY hour DESC
LIMIT :limit;
'''
