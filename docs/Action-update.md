# [LastfmLog](../README.md) - Action: `update`

Update the local database with data from the remote API.

On the first run, this will download all played tracks data. Subsequent runs are incremental, starting from the latest "playTime" stored in the database.


---


## Supported Options

- [--datadir](./Option-datadir.md)




## Example

```text
cli.py update
```

```text
downloading page:1 from:0 to:latest limit:200
33 more pages
downloading page:2
32 more pages
...
downloading page:33
1 more page
downloading page:34
saved 6420 tracks
```

```text
cli.py update
```

```text
downloading page:1 from:1685610645 to:latest limit:20
saved 9 tracks
```
