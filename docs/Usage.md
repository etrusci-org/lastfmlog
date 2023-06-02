# [LastfmLog](../README.md) - Usage

How to use it.


---


## Basics

```text
cli.py Action [Options...]
```

- **Action** is mandatory, while **Options** are optional.
- Multiple options can be combined together.
- It does not matter if the action comes before or after the options.
- Not all actions support the same options.




## Actions and Options Overview

You can also get an overview on the command line by using the `--help` (short: `-h`) option.

| Action  | Supported Options  |
|---------|--------------------|
| [testsecrets](./Action-testsecrets.md) | [--datadir](./Option-datadir.md) |
| [nowplaying](./Action-nowplaying.md) | [--datadir](./Option-datadir.md) |
| [update](./Action-update.md) | [--datadir](./Option-datadir.md) [--from](./Option-from.md) [--to](./Option-to.md) |
| [stats](./Action-stats.md) | [--datadir](./Option-datadir.md) [--limitall](./Option-limitall.md) [--limittopartists](./Option-limittopartists.md) [--limittoptracks](./Option-limittoptracks.md) [--limittopalbums](./Option-limittopalbums.md) [--limitplaysbyyear](./Option-limitplaysbyyear.md) [--limitplaysbymonth](./Option-limitplaysbymonth.md) [--limitplaysbyday](./Option-limitplaysbyday.md) [--limitplaysbyhour](./Option-limitplaysbyhour.md) |
| [export](./Action-export.md) | [--datadir](./Option-datadir.md) |
| [trimdatabase](./Action-trimdatabase.md) | [--datadir](./Option-datadir.md) |
| [resetdatabase](./Action-resetdatabase.md) | [--datadir](./Option-datadir.md) |
| [resetsecrets](./Action-resetsecrets.md) | [--datadir](./Option-datadir.md) |
