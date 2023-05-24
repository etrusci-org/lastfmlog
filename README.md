# LastfmLog

Command line tool that downloads your [Last.fm](https://last.fm) scrobbles (played tracks) data into a local database so you can do something with it.

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/etrusci-org/lastfmlog?include_prereleases&label=latest+release) ![GitHub issues](https://img.shields.io/github/issues/etrusci-org/lastfmlog)

- [Dependencies](#dependencies)
- [Install](#install)
- [First Time Setup](#first-time-setup)
- [Usage](#usage)
- [Database File](#database-file)
- [Statistics File](#statistics-file)
- [Secrets File Security](#secrets-file-security)
- [License](#license)

---

## Dependencies

- [Python](https://python.org) `>= 3.9.2`
- [Last.fm API Account](https://www.last.fm/api/account/create)

---

## Install

Copy the **lastfmlog/** directory to a location on your system where your user has read/write access.  
You can rename the copied directory if you want.  
You should end up with a directory structure like this:  
```text
lastfmlog/
├─ app/
│  ├─ data/           # default data directory
│  ├─ lastfmloglib/   # program files
│  ├─ cli.py          # command line interface
LICENSE.md
README.md
```

Optionally, make **lastfmlog/app/cli.py** executable so you can run it directly:

```text
cd lastfmlog/app/    # change into the app/ directory
chmod +x cli.py      # make the file executable
./cli.py             # run it
```
Alternatively, you can use the Python 3 binary on your system to run it:

```text
cd lastfmlog/app/    # change into the app/ directory
python3 cli.py       # run it
```

Both methods work; it's up to you. For the sake of simplicity in the documentation, it will be referred to as **cli.py**.

---

## First Time Setup

On the first run, you'll be asked for your API credentials. Here's how to get those:

1. Register an user account for you [here](https://www.last.fm/join) .
    - Username: this is the one you will enter in your secrets.
    - Email: your email address
2. Create an API account for LastfmLog [here](https://www.last.fm/api/account/create).
    - Contact email: your email address
    - Application name: whatever you want
    - Application description: whatever you want
    - Callback URL: leave empty
    - Application homepage: leave empty

Once you have created an API account, its data will be shown to you, or you can find it [here](https://www.last.fm/api/accounts) later. What you need is your **username** and **API key**.

Once you have your API credentials, it is recommended to run the `whoami` action first, since this will also validate them right away.  
Example:
```text
Creating secrets file: /path/to/lastfmlog/app/data/secrets.dat
See the README on how to get your API credentials. <https://github.com/etrusci-org/lastfmlog#readme>

Enter your Last.fm username: Scrobbler123
Enter your Last.fm API key: ***

Creating database file: /path/to/lastfmlog/app/data/database.sqlite3

[lastfmlog whoami]

      username: Scrobbler123
 registered on: 2023-01-01 11:22:33 UTC
         plays: 5907
       artists: 1088
        tracks: 3168
        albums: 1291
```

All good if you see a quick overview of your account at the end. If not, check your API credentials and delete the secrets file to getting asked again on the next run.

---

## Usage

Syntax: `cli.py Action [Options]...`

- **Action** is mandatory, while **Options** are optional.  
- Multiple options can be combined together.  
- It does not matter if the action comes before or after the options.  
- Not all actions support the same options.

Overview of available actions and options:

- **whoami**
  - `--datadir`
- **nowplaying**
  - `--datadir`
  - `--json`
- **update**
  - `--datadir`
  - `--from`
  - `--to`
  - `--verbose`
- **reset**
  - `--datadir`
- **stats**
  - `--datadir`
  - `--limittopartists`
  - `--limittoptracks`
  - `--limittopalbums`
  - `--limitplaysbyyear`
  - `--limitplaysbymonth`
  - `--limitplaysbyday`
  - `--limitplaysbyhour`

### Actions

#### whoami

See who you are authenticated as. Useful for testing if your secrets are valid. Uses remote API data.  
Example:
```text
cli.py whoami
```

#### nowplaying

Show currently playing track. Uses remote API data.  
Example:
```text
cli.py nowplaying
```

#### update

Update the local database with data from the remote API.  
Example:
```text
cli.py update
```

#### stats

Generate statistics with data from the local database and save the output to a file.  
Example:
```text
cli.py stats
```

#### reset

Reset all database contents. Note that there will be no confirmation prompt.  
Example:
```text
cli.py reset
```

### Options

#### --help, -h

Applies to action: *all*

Show an overview of the available actions and options.  
Example:
```text
cli.py --help
cli.py -h
```

#### --datadir PATH

Applies to action: *all*

Override the default data directory path. You must create it first. It will not be created just by using this option. Each API account has its own data directory. Therefore you can switch between multiple users/accounts by using this option.  
Example:
```text
cli.py whoami --datadir /tmp/batman
cli.py whoami --datadir /tmp/joker
```

#### --json

Applies to action: `nowplaying`

Show JSON instead of text output.  
Example:
```text
cli.py nowplaying --json
```

#### --from UNIXTIME

Applies to action: `update`

Only fetch plays after this time. Unixtime stamp must be in UTC.  
Example:
```text
cli.py update --from 1684769072
```

#### --to UNIXTIME

Applies to action: `update`

Only fetch plays before this time. Unixtime stamp must be in UTC.  
Example:
```text
cli.py update 
cli.py update --to 1684847504
```

#### --verbose, -v

Applies to action: `update`

Show fetched tracks while updating.  
Example:
```text
cli.py update --verbose
cli.py update -v
```

#### --limittopartists NUMBER

Applies to action: `stats`

Limit the number of items in top artists.  
Example:
```text
cli.py stats --limittopartists 10
```

#### --limittoptracks NUMBER

Applies to action: `stats`

Limit the number of items in top tracks.  
Example:
```text
cli.py stats --limittoptracks 10
```

#### --limittopalbums NUMBER

Applies to action: `stats`

Limit the number of items in top albums.  
Example:
```text
cli.py stats --limittopalbums 10
```

#### --limitplaysbyyear NUMBER

Applies to action: `stats`

Limit the number of items in plays by year.  
Example:
```text
cli.py stats --limitplaysbyyear 5
```

#### --limitplaysbymonth NUMBER

Applies to action: `stats`

Limit the number of items in plays by month.  
Example:
```text
cli.py stats --limitplaysbymonth 12
```

#### --limitplaysbyday NUMBER

Applies to action: `stats`

Limit the number of items in plays by day.  
Example:
```text
cli.py stats --limitplaysbyday 30
```

#### --limitplaysbyhour NUMBER

Applies to action: `stats`

Limit the number of items in plays by hour.  
Example:
```text
cli.py stats --limitplaysbyhour 24
```

---

## Database File

Default path: **lastfmlog/app/data/database.sqlite3**  
Engine: [SQLite3](https://sqlite.org)  
Schema:
```sql
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
```

**playTime** (UTC), **artist**, **track** and **album** come directly from the API.  

The **playHash** is is generated with the method `_getPlayHash()` in **lastfmlog/app/lastfmloglib/app.py**:  
```python
@staticmethod
def _getPlayHash(track: dict) -> str:
    raw = str(track['date']['uts'] + track['artist']['name'] + track['name'] + track['album']['#text']).lower()
    return hashlib.sha256(raw.encode()).hexdigest()
```

---

## Statistics File

Default path: **lastfmlog/app/data/stats.json**  
Format: [JSON](https://json.org)  
Example:
```json
{
    "_username": "Scrobbler123",
    "_statsModifiedOn": 1684843128,
    "_databaseModifiedOn": 1684843126,
    "__localTimezoneOffset": 7200,
    "totalPlays": 5988,
    "uniqueArtists": 1089,
    "uniqueTracks": 3194,
    "uniqueAlbums": 1295,
    "topArtists": [
        {
            "plays": 409,
            "artist": "EtheReal Media™"
        },
        {
            "plays": 252,
            "artist": "Romeo Rucha"
        },
        {
            "plays": 208,
            "artist": "Spartalien"
        },
        //...
    ],
    "topTracks": [
        {
            "plays": 16,
            "artist": "Yuki Kajiura",
            "track": "In Memory Of You"
        },
        {
            "plays": 16,
            "artist": "DJ Unknown Face",
            "track": "Dat's Cool"
        },
        {
            "plays": 16,
            "artist": "Dead Calm",
            "track": "Searchin'"
        },
        //...
    ],
    "topAlbums": [
        {
            "plays": 161,
            "artist": "Various Artists",
            "album": "BIZCAS10: Ten Years of Business Casual"
        },
        {
            "plays": 145,
            "artist": "Various Artists",
            "album": "Conversions - A K&D Selection"
        },
        {
            "plays": 141,
            "artist": "Various Artists",
            "album": "Aesthetic Vibes"
        },
        //...
    ],
    "playsByYear": [
        {
            "plays": 5502,
            "year": "2023"
        },
        {
            "plays": 486,
            "year": "2022"
        }
    ],
    "playsByMonth": [
        {
            "plays": 1836,
            "month": "2023-05"
        },
        {
            "plays": 1743,
            "month": "2023-04"
        },
        {
            "plays": 508,
            "month": "2023-03"
        },
        //...
    ],
    "playsByDay": [
        {
            "plays": 4,
            "day": "2023-05-23"
        },
        {
            "plays": 119,
            "day": "2023-05-22"
        },
        {
            "plays": 78,
            "day": "2023-05-21"
        },
        //...
    ],
    "playsByHour": [
        {
            "plays": 4,
            "hour": "13",
            "day": "2023-05-23"
        },
        {
            "plays": 20,
            "hour": "00",
            "day": "2023-05-23"
        },
        {
            "plays": 11,
            "hour": "23",
            "day": "2023-05-22"
        },
        //...
    ]
}
```

---

## Secrets File Security

Please keep in mind that anyone who has access to the filesystem on which your data directory is stored, can decode and read your secrets file with little knowledge.

---

## License

See [LICENSE](./LICENSE.md).

---
