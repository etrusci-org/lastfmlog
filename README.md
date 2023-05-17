# LastfmLog

Download your [Last.fm](https://last.fm) scrobbles data into a local database to do stuff with it.

---

## How to run it

You don't have to install this. Just put the `app/` directory on a disk where your user has read/write access.

<!-- TODO: explain how to create secrets file -->

Make `app/cli.py` executable so you can run it directly:

```bash
cd app/            # change into app/ directory
chmod +x cli.py    # make the file executable
./cli.py           # run it
```

Or use the Python 3 binary on your system to run it:

```bash
cd app/           # change into app/ directory
python3 cli.py    # run it
```

Either way works, it's up to you. Just for documentation simplification, this will be written as just `cli.py` from now on.

---

## What to do with it

```text
cli.py <action> [options]
```

**action** is mandatory (`<...>`).  
**options** are optional (`[...]`).


### Actions

`update`  
Update local database with data from remote API. On the first run, all plays will be fetched. Afterwards only plays that are younger than the last one stored in local database.
Example output:
```text
Fetching data page 1
+ The Gentle People - Journey (DMX Krew remix)
+ Insect Jazz - Wildflower
+ Patchwork - Frequencies
Fetched 3 new tracks
Skipped 0 tracks
```

`stats`  
Bake statistics from data in local database.  
Example output:
```text
Local database has 5483 tracks stored and was changed 53m ago
Update database first? [Y/n]: y
Fetching data page 1
+ Fila Brazillia - A Zed & Two L's
+ Funki Porcini - It's a Long Road
+ Chin Chillaz - Konkret
Fetched 3 new tracks
Skipped 0 tracks
Stats saved to file: /home/user/lastfmlog/app/data/stats.json
```

`reset`  
Delete everything in local database.
Example output:
```text
Reset database? [Y/n]: y
Deleted 5495 tracks
```

#### Global options

`-d PATH` or `--datadir PATH`  
Override default data directory path.  
Default: `app/data/`

#### Options for `update`

`--updatefromstart`  
Fetch tracks from the beginning of time. In case you deleted some rows in your local database but don't want to use the `reset` action for some reason.
Default: *incremental update*

#### Options for `stats`

`-o SECONDS` or `--obsoleteafter SECONDS`  
Time in seconds until the database is considered obsolete and you will be asked if you want to update it first.  
Default: `1800`

`--playsbyyearlimit NUMBER`  
Limit the number of items in *plays by year*.  
Default: *unlimited*

`--playsbymonthlimit NUMBER`  
Limit the number of items in *plays by month*.  
Default: *unlimited*

`--playsbydaylimit NUMBER`  
Limit the number of items in *plays by day*.  
Default: *unlimited*

`--playsbyhourlimit NUMBER`  
Limit the number of items in *plays by hour*.  
Default: *unlimited*

`--topartistslimit NUMBER`  
Limit the number of items in *top artists*.  
Default: *unlimited*

`--toptrackslimit NUMBER`  
Limit the number of items in *top tracks*.  
Default: *unlimited*

`--topalbumslimit NUMBER`  
Limit the number of items in *top albums*.  
Default: *unlimited*

---
