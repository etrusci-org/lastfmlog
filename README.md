# LastfmLog

Command line tool to download your [Last.fm](https://last.fm) scrobbles *(played tracks)* data into a local database so you can do stuff with it.

---

## Requirements

- Python >= 3.9.2
- A free [Last.fm](https://www.last.fm/join) user account

---

## Installing

1. Copy the `app/` directory to a location on your system where your user has read/write access.

2. Copy `app/data/secrets.example.json` to `app/data/secrets.json` and open it in a text editor. Insert your Last.fm username as the `apiUser` value and your secret API key as the `apiKey` value. You can create your API credentials [here](https://www.last.fm/api/accounts).

3. Optionally, make `app/cli.py` executable so you can run it directly:


```bash
cd app/            # change into the app/ directory
chmod +x cli.py    # make the file executable
./cli.py           # run it
```

Alternatively, you can use the Python 3 binary on your system to run it:

```bash
cd app/           # change into the app/ directory
python3 cli.py    # run it
```

Both methods work; it's up to you. For the sake of simplicity in the documentation, it will be referred to as `cli.py` from now on.

---

## Usage

`cli.py Action [Options]...`

**Action** is mandatory, while **options** are optional.

You can always use `--help` or `-h` for a quick overview of the available options. For more detailed explanations, please continue reading.

### Actions

Only one action can be executed at a time.

#### update

Update the local database with data from the remote API. On the first run, all plays will be fetched. Afterward, only plays that are more recent than the last one stored in the local database will be fetched.  
Example:
```bash
cli.py update
# Fetching data page 1
# + The Gentle People - Journey (DMX Krew remix)
# + Insect Jazz - Wildflower
# + Patchwork - Frequencies
# Fetched 3 new tracks
# Skipped 0 tracks
```

#### stats

Generate statistics from the data in the local database.  
Example:
```bash
cli.py stats
# Stats saved to file: /home/user/lastfmlog/app/data/stats.json
```

#### reset

Delete everything in the local database.  
Example:
```bash
cli.py reset
# Reset database? [Y/n]: y
# Deleted 5495 tracks
```

### Options

Multiple options can be set at once.

#### (*global*) --datadir PATH

Override the default data directory path.  
Default: `app/data/`  
Example: `cli.py update --datadir /mnt/foo/mydatadir`

#### (*update*) --from UNIXTIME

Only fetch plays after this time.  
Default: *incremental update*  
Example: `cli.py update --from 1684443099`

#### (*update*) --to UNIXTIME

Only fetch plays before this time.  
Default: *incremental update*  
Example: `cli.py update --to 1684443099`

#### (*stats*) --obsoleteafter SECONDS

Set the time in seconds until the database is considered obsolete, and you will be asked if you want to update it first. Set to `-1` to disable this check.  
Default: `1800`  
Example: `cli.py stats --obsoleteafter 900`

#### (*stats*) --playsbyyearlimit NUMBER

Limit the number of items in *plays by year*.  
Default: *unlimited*  
Example: `cli.py stats --playsbyyearlimit 10`

#### (*stats*) --playsbymonthlimit NUMBER

Limit the number of items in *plays by month*.  
Default: *unlimited*  
Example: `cli.py stats --playsbymonthlimit 12`

#### (*stats*) --playsbydaylimit NUMBER

Limit the number of items in *plays by day*.  
Default: *unlimited*  
Example: `cli.py stats --playsbydaylimit 7`

#### (*stats*) --playsbyhourlimit NUMBER

Limit the number of items in *plays by hour*.  
Default: *unlimited*  
Example: `cli.py stats --playsbyhourlimit 24`

#### (*stats*) --topartistslimit NUMBER

Limit the number of items in *top artists*.  
Default: *unlimited*  
Example: `cli.py stats --topartistslimit 10`

#### (*stats*) --toptrackslimit NUMBER

Limit the number of items in *top tracks*.  
Default: *unlimited*  
Example: `cli.py stats --toptrackslimit 10`

#### (*stats*) --topalbumslimit NUMBER

Limit the number of items in *top albums*.  
Default: *unlimited*  
Example: `cli.py stats --topalbumslimit 10`

---
