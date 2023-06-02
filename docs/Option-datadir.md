# [LastfmLog](../README.md) - Option: `--datadir`

`--datadir PATH`

Applies to action: *all*

Override the default data directory path. The directory PATH points to, must exist. Each API account has its own data directory. Therefore you can switch between multiple users/accounts by using this option.


---


## Example

```text
cli.py testsecrets --datadir /tmp/batman
```

```text
      username: Batman
  profile link: https://www.last.fm/user/Batman
 registered on: 2022-11-03 11:46:00 UTC
data directory: /tmp/batman
```

```text
cli.py testsecrets --datadir /tmp/joker
```

```text
      username: Joker
  profile link: https://www.last.fm/user/Joker
 registered on: 2021-10-02 10:35:59 UTC
data directory: /tmp/joker
```
