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
