# [LastfmLog](../README.md) - Secrets File

Where your statistics are exported to.

**Filename**: stats.json  
**Format**: [JSON](https://json.org)


---


## Example

You can find an example on how to use the generated JSON file in [example/php-stats-json.php](../example/php-stats-json.php).

```text
cli.py stats --limitall 3
```


```json
{
    "_username": "DemoUser123",
    "_statsModifiedOn": 1685620285,
    "_databaseModifiedOn": 1685617402,
    "_localTimezoneOffset": 7200,
    "playsTotal": 6419,
    "plays7days": {
        "plays": 308,
        "average": 44
    },
    "plays14days": {
        "plays": 870,
        "average": 62
    },
    "plays30days": {
        "plays": 2221,
        "average": 74
    },
    "plays90days": {
        "plays": 4400,
        "average": 48
    },
    "plays180days": {
        "plays": 6419,
        "average": 35
    },
    "plays365days": {
        "plays": 6419,
        "average": 17
    },
    "uniqueArtists": 1156,
    "uniqueTracks": 3363,
    "uniqueAlbums": 1376,
    "topArtists": [
        {
            "plays": 447,
            "artist": "EtheReal Media™"
        },
        {
            "plays": 252,
            "artist": "Romeo Rucha"
        },
        {
            "plays": 208,
            "artist": "Spartalien"
        }
    ],
    "topTracks": [
        {
            "plays": 19,
            "artist": "EtheReal Media™",
            "track": "Ｓｕｎｎｙ Ｓｋｉｅｓ"
        },
        {
            "plays": 17,
            "artist": "EtheReal Media™",
            "track": "Ｔｏｄａｙ'ｓ Ｏｕｔｌｏｏｋ"
        },
        {
            "plays": 17,
            "artist": "EtheReal Media™",
            "track": "Ｅｖｅｎｉｎｇ Ｂｒｅｅｚｅ"
        }
    ],
    "topAlbums": [
        {
            "plays": 161,
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
        }
    ],
    "playsByYear": [
        {
            "plays": 5935,
            "year": "2023"
        },
        {
            "plays": 484,
            "year": "2022"
        }
    ],
    "playsByMonth": [
        {
            "plays": 13,
            "month": "2023-06"
        },
        {
            "plays": 2256,
            "month": "2023-05"
        },
        {
            "plays": 1743,
            "month": "2023-04"
        }
    ],
    "playsByDay": [
        {
            "plays": 13,
            "day": "2023-06-01"
        },
        {
            "plays": 33,
            "day": "2023-05-31"
        },
        {
            "plays": 34,
            "day": "2023-05-30"
        }
    ],
    "playsByHour": [
        {
            "plays": 3,
            "hour": "2023-06-01 12"
        },
        {
            "plays": 9,
            "hour": "2023-06-01 11"
        },
        {
            "plays": 1,
            "hour": "2023-06-01 10"
        }
    ]
}
```
