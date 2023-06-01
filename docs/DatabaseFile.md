# [LastfmLog](../README.md) - Database File

Where your data is stored.

**Filename**: database.sqlite3  
**Engine**: [SQLite3](https://sqlite.org)


---


## Schema

```sql
BEGIN TRANSACTION;

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
```

**playTime** (UTC), **artist**, **track** and **album** come directly from the API.

The **playHash**, which is used to uniquely identify a play, is generated with the method **_getPlayHash()** in **lastfmlog/app/lastfmloglib/app.py**.

```python
@staticmethod
def _getPlayHash(track: dict) -> str:
    raw = str(
        track['date']['uts']
        + track['artist']['name']
        + track['name']
        + track['album']['#text']
    ).lower()

    return hashlib.sha256(raw.encode()).hexdigest()
```
