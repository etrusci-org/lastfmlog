# [LastfmLog](../README.md) - Install

How to make it work.

**Note:** Although it's written in Python, it's not meant to be a module and was not tested this way. If you want to use it as a module, you have to figure it out on your own. I use it as described in this document.


---


## 1. Copy App Files

Copy the **lastfmlog/** directory to a location on your system where your user has **read+write** access.  
You can rename the copied directory if you want.  
You should end up with a directory structure like this:

```text
lastfmlog/
├─ app/
│  ├─ data/           # default data directory
│  ├─ lastfmloglib/   # program files
│  ├─ cli.py          # command line interface
├─ docs/
├─ example/
LICENSE.md
README.md
```




## 2. Make cli.py Executable

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




## 3. First Time Setup

On the first run, you'll be asked for your API credentials. See [Dependencies](./Dependencies.md) on how to get those. It's recommended to run the `testsecrets` action first, since this will also validate them right away.  
Example:

```text
cli.py testsecrets
```

```text
creating secrets file
see the README on how to get your API credentials. <https://github.com/etrusci-org/lastfmlog#readme>

enter your Last.fm username: DemoUser123
enter your Last.fm API key (input will be hidden): 

      username: DemoUser123
  profile link: https://www.last.fm/user/DemoUser123
 registered on: 2022-11-03 11:46:00 UTC
data directory: /path/to/lastfmlog/app/data
```

All good if you see a quick overview of your account at the end. If not, check your API credentials and use the `resetsecrets` to getting asked again on the next run.
