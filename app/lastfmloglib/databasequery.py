databaseQuery = {}

# Insert new track into tracklog
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

# Reset all tables (transaction)
databaseQuery['resetDatabase'] = '''
BEGIN;
DELETE FROM trackslog;
COMMIT;
'''

# Total plays
databaseQuery['playsTotal'] = '''
SELECT COUNT(playHash)
FROM trackslog;
'''

# Unique artists
databaseQuery['uniqueArtists'] = '''
SELECT COUNT(DISTINCT artist COLLATE NOCASE)
FROM trackslog;
'''

# Unique tracks
databaseQuery['uniqueTracks'] = '''
SELECT COUNT(DISTINCT artist || track COLLATE NOCASE)
FROM trackslog;
'''

# Unique albums
databaseQuery['uniqueAlbums'] = '''
SELECT COUNT(DISTINCT artist || album COLLATE NOCASE)
FROM trackslog;
'''

# Top artists
databaseQuery['topArtists'] = '''
SELECT artist, COUNT(artist) AS plays
FROM trackslog
GROUP BY artist COLLATE NOCASE
ORDER BY plays DESC
LIMIT :limit;
'''

# Top tracks
databaseQuery['topTracks'] = '''
SELECT artist, track, COUNT(artist || track COLLATE NOCASE) AS plays
FROM trackslog GROUP BY (artist || track COLLATE NOCASE)
ORDER BY plays DESC
LIMIT :limit;
'''

# Top albums
databaseQuery['topAlbums'] = '''
SELECT CASE WHEN COUNT(DISTINCT artist) > 1 THEN 'Various Artists' ELSE MAX(artist) END AS artist, album, COUNT(album) AS plays
FROM trackslog
WHERE album IS NOT NULL
GROUP BY album COLLATE NOCASE
ORDER BY plays DESC
LIMIT :limit;
'''

# Plays by year
databaseQuery['playsByYear'] = '''
SELECT strftime('%Y', playTime, 'unixepoch') AS year, COUNT(playHash) AS plays
FROM trackslog
GROUP BY year
ORDER BY year DESC
LIMIT :limit;
'''

# Plays by month
databaseQuery['playsByMonth'] = '''
SELECT strftime('%Y-%m', playTime, 'unixepoch') AS month, COUNT(playHash) AS plays
FROM trackslog
GROUP BY month
ORDER BY month DESC
LIMIT :limit;
'''

# Plays by day
databaseQuery['playsByDay'] = '''
SELECT strftime('%Y-%m-%d', playTime, 'unixepoch') AS day, COUNT(playHash) AS plays
FROM trackslog
GROUP BY day
ORDER BY day DESC
LIMIT :limit;
'''

# Plays by hour
databaseQuery['playsByHour'] = '''
SELECT strftime('%Y-%m-%d %H', playTime, 'unixepoch') AS hour, COUNT(playHash) AS plays
FROM trackslog
GROUP BY hour
ORDER BY hour DESC
LIMIT :limit;
'''
