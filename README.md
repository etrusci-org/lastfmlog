# LastfmLog

Command line tool that downloads your [Last.fm](https://last.fm) scrobbles (played tracks) data into a local database so you can do something with it.

[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/etrusci-org/lastfmlog?include_prereleases&label=latest+release)](https://github.com/etrusci-org/lastfmlog/releases) [![GitHub issues](https://img.shields.io/github/issues/etrusci-org/lastfmlog)](https://github.com/etrusci-org/lastfmlog/issues)

- [Dependencies](#dependencies)
- [Install](#install)
- [First Time Setup](#first-time-setup)
- [Usage](#usage)
  - [Actions](#actions)
  - [Options](#options)
- [Database File](#database-file)
- [Secrets File](#secrets-file)
- [Statistics File](#statistics-file)
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
Creating secrets file
See the README on how to get your API credentials. <https://github.com/etrusci-org/lastfmlog#readme>

Enter your Last.fm username: Scrobbler123
Enter your Last.fm API key (input will be hidden):

[lastfmlog whoami]

data directory: /path/to/lastfmlog/app/data
      username: Scrobbler123
 registered on: 2022-11-03 11:46:00 UTC
         plays: 6288
       artists: 1148
        tracks: 3291
        albums: 1355
```

All good if you see a quick overview of your account at the end. If not, check your API credentials and delete the secrets file to getting asked again on the next run.

---

## Usage

Syntax: `cli.py Action [Options ...]`

- **Action** is mandatory, while **Options** are optional.  
- Multiple options can be combined together.  
- It does not matter if the action comes before or after the options.  
- Not all actions support the same options.

Overview of available actions and the options they support:

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
- **stats**
  - `--datadir`
  - `--limittopartists`
  - `--limittoptracks`
  - `--limittopalbums`
  - `--limitplaysbyyear`
  - `--limitplaysbymonth`
  - `--limitplaysbyday`
  - `--limitplaysbyhour`
- **export**
  - `--datadir`
- **resetdatabase**
  - `--datadir`
- **resetsecrets**
  - `--datadir`

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

### export

Dump the database as SQL source code to a file.  
Example:
```text
cli.py export
```

#### resetdatabase

Reset all database contents. Note that there will be no confirmation prompt.
Alternatively, you could manually delete the database file.  
Example:
```text
cli.py resetdatabase
```

#### resetsecrets

Reset secrets. You will be asked to enter your API credentials again on the next run. Note that there will be no confirmation prompt.
Alternatively, you could manually delete the secrets file.  
Example:
```text
cli.py resetsecrets
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

The **playHash**, which is used to uniquely identify a play, is generated with the method `_getPlayHash()` in **lastfmlog/app/lastfmloglib/app.py**:  
```python
@staticmethod
def _getPlayHash(track: dict) -> str:
    raw = str(track['date']['uts'] + track['artist']['name'] + track['name'] + track['album']['#text']).lower()
    return hashlib.sha256(raw.encode()).hexdigest()
```

---

## Secrets File

Default path: **lastfmlog/app/data/secrets.dat**  
Format: [JSON](https://json.org) encoded with [Base64](https://en.wikipedia.org/wiki/Base64).

Please keep in mind that anyone who has read-access to the filesystem on which your data directory is stored, can decode and read your secrets file with little knowledge. Therefore, if you put this on a webserver, you must have the data directory outside of the public document root.

---

## Statistics File

Default path: **lastfmlog/app/data/stats.json**  
Format: [JSON](https://json.org)  
Example:
```json
{
    "_username": "SPARTALIEN",
    "_statsModifiedOn": 1685187850,
    "_databaseModifiedOn": 1685187386,
    "_localTimezoneOffset": 7200,
    "playsTotal": 6287,
    "plays7days": {
        "plays": 598,
        "average": 85
    },
    "plays14days": {
        "plays": 1326,
        "average": 94
    },
    "plays30days": {
        "plays": 2327,
        "average": 77
    },
    "plays90days": {
        "plays": 4424,
        "average": 49
    },
    "plays180days": {
        "plays": 6287,
        "average": 34
    },
    "plays365days": {
        "plays": 6287,
        "average": 17
    },
    "uniqueArtists": 1148,
    "uniqueTracks": 3291,
    "uniqueAlbums": 1355,
    "topArtists": [
        {
            "plays": 459,
            "artist": "EtheReal Media™"
        },
        {
            "plays": 252,
            "artist": "Romeo Rucha"
        },
        {
            "plays": 209,
            "artist": "Spartalien"
        },
        ...
    ],
    "topTracks": [
        {
            "plays": 17,
            "artist": "EtheReal Media™",
            "track": "Ｓｕｎｎｙ Ｓｋｉｅｓ"
        },
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
        ...
    ],
    "topAlbums": [
        {
            "plays": 174,
            "artist": "Various Artists",
            "album": "Aesthetic Vibes"
        },
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
        ...
    ],
    "playsByYear": [
        {
            "plays": 5801,
            "year": "2023"
        },
        {
            "plays": 486,
            "year": "2022"
        }
    ],
    "playsByMonth": [
        {
            "plays": 2135,
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
        ...
    ],
    "playsByDay": [
        {
            "plays": 27,
            "day": "2023-05-27"
        },
        {
            "plays": 84,
            "day": "2023-05-26"
        },
        {
            "plays": 91,
            "day": "2023-05-25"
        },
        ...
    ],
    "playsByHour": [
        {
            "plays": 1,
            "hour": "2023-05-27 13"
        },
        {
            "plays": 9,
            "hour": "2023-05-27 12"
        },
        {
            "plays": 11,
            "hour": "2023-05-27 11"
        },
        ...
    ]
}
```

---

## License

See [LICENSE](./LICENSE.md).

---
