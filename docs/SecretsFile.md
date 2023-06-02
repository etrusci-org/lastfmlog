# [LastfmLog](../README.md) - Secrets File

Where your secrets are stored.

**Filename**: secrets.bin  
**Format**: [JSON](https://json.org) encoded with [Base64](https://en.wikipedia.org/wiki/Base64)


---


## Security

Please keep in mind that anyone who has read-access to the filesystem on which your data directory is stored, can decode and read your secrets file with little knowledge. If you put this on a webserver, you must have the data directory outside of the public document root.
