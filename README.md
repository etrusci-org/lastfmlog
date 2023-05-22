# LastfmLog

Command line tool that downloads your [Last.fm](https://last.fm) scrobbles *(played tracks)* data into a local database so you can do something with it.

---

## Dependencies

- [Python](https://python.org) `>= 3.9.2`
- [Last.fm API Account](https://www.last.fm/api/account/create)

---

## Install

Copy the **app/** directory to a location on your system where your user has read/write access.  
You can rename the copied directory if you want - e.g. **lastfmlog-app**, **lastfmlog**, or **whatever** you want it to be.  
You should end up with a directory structure like this:

```text
app/
    data/
    lastfmloglib/
    cli.py
```

Optionally, make **app/cli.py** executable so you can run it directly:

```text
cd app/            # change into the app/ directory
chmod +x cli.py    # make the file executable
./cli.py           # run it
```
Alternatively, you can use the Python 3 binary on your system to run it:

```text
cd app/           # change into the app/ directory
python3 cli.py    # run it
```

Both methods work; it's up to you. For the sake of simplicity in the documentation, it will be referred to as **cli.py**.

---

## First Time Setup

Before the LastfmLog can do its job, it must have a database and secrets file in the data directory. Those will be generated automagically the first time you run an action.  
In any case, on the first run, you'll be asked for your API credentials. But those you must create on your own.

1. Register an user account for you [here](https://www.last.fm/join).
    - Username: this is the one you will enter in your secrets.
    - Email: your email address
2. Create an API account for LastfmLog [here](https://www.last.fm/api/account/create).
    - Contact email: your email address
    - Application name: whatever you want
    - Application description: whatever you want
    - Callback URL: leave empty
    - Application homepage: leave empty

Once you have created an API account, its data will be shown to you, or you can find it [here](https://www.last.fm/api/accounts) later.

Once you have your API credentials, it is recommended to run the `whoami` action first, since this will also validate them right away.  
Example:
```text
cli.py whoami

Creating secrets file: /path/to/app/data/secrets.json

No worries if you make mistakes, you can edit the file in a text editor.
See the README on how to get an API key.

Enter your Last.fm username: Scrobbler123
Enter your Last.fm API key: ***

Creating database file: /path/to/app/data/database.sqlite3

      username: Scrobbler123
 registered on: 2023-01-01 11:22:33 UTC
         plays: 5907
       artists: 1088
        tracks: 3168
        albums: 1291
```

All good if you see a quick overview of your account at the end. If not, check your API credentials again. You can either edit the secrets file in a text editor or delete it to getting asked again on the next run.

---

## Usage

Syntax: `cli.py Action [Options]...`

**Action** is mandatory, while **Options** are optional. Multiple options can be combined together. It does not matter if the action comes before or after the options. Not all actions support the same options.

Overview:

| Action | Options                                    |
|--------|--------------------------------------------|
| whoami | `--datadir`                                |
| update | `--datadir`, `--from`, `--to`, `--verbose` |
| stats  | `--datadir`                                |
| reset  | `--datadir`                                |

### Actions

#### whoami

See who you are authenticated as. Useful for testing if your secrets are valid.  
Example:
```text
cli.py whoami
```

#### update

Update the local database with data from the remote API.  
Example:
```text
cli.py update
```

#### stats

Generate statistics file.  
Example:
```text
./cli.py stats
```

#### reset

Reset database contents.  
Example:
```text
./cli.py reset
```

### Options

#### --datadir PATH

Applies to action: *all*

Override the default data directory path. You must create it first since it will not be created just by using this option. Each API account has its own data directory. Therefore you can switch between multiple accounts by using this option.
Example:
```text
./cli.py whoami --datadir /tmp/batman
./cli.py whoami --datadir /tmp/joker
```

#### --from UNIXTIME

Applies to action: `update`

Only fetch plays after this time. Unixtime stamp must be in UTC.  
Example:
```text
./cli.py update --from 1684769072
```

#### --to UNIXTIME

Applies to action: `update`

Only fetch plays before this time. Unixtime stamp must be in UTC.  
Example:
```text
./cli.py update 
./cli.py update --to 1684847504
```

#### --verbose, -v

Applies to action: `update`

Show fetched tracks while updating.  
Example:
```text
./cli.py update --verbose
./cli.py update -v
```

---

## License

See [LICENSE](./LICENSE.md).

---
