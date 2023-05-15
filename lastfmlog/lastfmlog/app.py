import os
import json
import urllib.request
import hashlib
import time

from .database import DatabaseSQLite
from .database_schema import databaseSchema



class App:
    conf: dict
    args: dict
    dataDir: str
    dbFile: str
    secrets: dict
    lastPlayedOnTime: int = -1
    DB: DatabaseSQLite


    def __init__(self, conf: dict, args: dict) -> None:
        # 'member
        self.conf = conf
        self.args = args

        # Assume crucial paths and check them
        self.dataDir = args['datadir'] if args['datadir'] else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.secretsFile = os.path.join(self.dataDir, 'secrets.json')

        try:
            if not os.path.isdir(self.dataDir):
                raise FileNotFoundError(f'Data directory path does not exist or is not a directory: {self.dataDir}')
            if not os.path.isfile(self.secretsFile):
                raise FileNotFoundError(f'Secrets file path does not exist or is not a file: {self.secretsFile}')
        except FileNotFoundError as e:
            print(e)
            exit(1)

        # Load secrets
        try:
            with open(self.secretsFile) as f:
                self.secrets = json.load(f)
        except json.JSONDecodeError as e:
            print(f'Error while decoding secrets file. {e}')
            exit(1)

        # Data dir and secrets file are ok if we reach this line,
        # therefore we can now create the database file if it does not exist already
        self.dbFile = os.path.join(self.dataDir, 'main.sqlite3')
        self.DB = DatabaseSQLite(dbFile=self.dbFile)
        if not os.path.isfile(self.dbFile):
            self._createDatabase()


    def update(self) -> None:
        self.lastPlayedOnTime = self._getLastPlayedOnTime()
        self._fetchRecentTracks()
        self.DB.vacuum()


    def stats(self) -> None:
        con, cur = self.DB.connect()

        stats = {
            'totalScrobbles': 0,
            'uniqueArtistsCount': 0,
            'uniqueTracksCount': 0,
            'uniqueAlbumsCount': 0,
            'topArtists': [],
            'topTracks': [],
            'topAlbums': [],
        }

        # Total scrobbles
        q = 'SELECT COUNT(DISTINCT scrobbleHash) FROM trackslog;'
        cur.execute(q)
        stats['totalScrobbles'] = cur.fetchone()[0]

        # Unique artists
        q = 'SELECT COUNT(DISTINCT artistName COLLATE NOCASE) FROM trackslog;'
        cur.execute(q)
        stats['uniqueArtistsCount'] = cur.fetchone()[0]

        # Unique tracks
        q = 'SELECT COUNT(DISTINCT artistName || trackName COLLATE NOCASE) FROM trackslog;'
        cur.execute(q)
        stats['uniqueTracksCount'] = cur.fetchone()[0]

        # Unique albums
        q = 'SELECT COUNT(DISTINCT artistName || albumName COLLATE NOCASE) FROM trackslog;'
        cur.execute(q)
        stats['uniqueAlbumsCount'] = cur.fetchone()[0]

        # Top artists
        q = 'SELECT artistName, COUNT(artistName) AS playCount FROM trackslog GROUP BY artistName COLLATE NOCASE ORDER BY playCount DESC LIMIT ?;'
        v = [
            self.args['limit'] if self.args['limit'] else 100
        ]
        cur.execute(q, v)
        for v in cur.fetchall():
            stats['topArtists'].append({
                'count': v[1],
                'artist': v[0],
            })

        # Top tracks
        q = 'SELECT artistName, trackName, COUNT(trackName) AS playCount FROM trackslog GROUP BY trackName COLLATE NOCASE ORDER BY playCount DESC LIMIT ?;'
        v = [
            self.args['limit'] if self.args['limit'] else 100
        ]
        cur.execute(q, v)
        for v in cur.fetchall():
            stats['topTracks'].append({
                'count': v[2],
                'track': v[1],
                'artist': v[0],
            })

        # Top albums
        q = 'SELECT CASE WHEN COUNT(DISTINCT artistName) > 1 THEN \'Various Artists\' ELSE MAX(artistName) END AS artistName, albumName, COUNT(albumName) AS playCount FROM trackslog GROUP BY albumName COLLATE NOCASE ORDER BY playCount DESC LIMIT ?;'
        v = [
            self.args['limit'] if self.args['limit'] else 100
        ]
        cur.execute(q, v)
        for v in cur.fetchall():
            stats['topAlbums'].append({
                'count': v[2],
                'album': v[1],
                'artist': v[0],
            })

        con.close()

        # Also save the stats to a file
        statsFile = os.path.join(self.dataDir, 'stats.json')
        with open(statsFile, mode='w') as f:
            f.write(json.dumps(stats, ensure_ascii=False, indent=4))
            print(f'> Stats saved to file: {statsFile}')


    def _createDatabase(self) -> None:
        con, cur = self.DB.connect()
        try:
            cur.executescript(databaseSchema)
        except Exception as e:
            print(f'Error while creating database: {e}')
        finally:
            con.close()


    def _getLastPlayedOnTime(self) -> int:
        con, cur = self.DB.connect()
        q = 'SELECT playedOnTime FROM trackslog LIMIT 1;'
        cur.execute(q)
        dump = cur.fetchone()
        con.close()
        return dump[0] if dump else self.lastPlayedOnTime


    def _fetchRecentTracks(self, page: int = 1) -> None:
        # Bake API url
        url  = self.conf['apiBaseURL']
        url += '?method=user.getrecenttracks'
        url += '&format=json'
        url += '&extended=0'
        url += f'&limit={self.conf["apiItemsPerPageLimitInitial"] if self.lastPlayedOnTime == -1 else self.conf["apiItemsPerPageLimitIncremental"]}'
        url += f'&from={self.lastPlayedOnTime + 1}'
        url += f'&page={page}'
        url += f'&user={self.secrets["apiUser"]}'
        url += f'&api_key={self.secrets["apiKey"]}'

        print(f'> Fetching data page {page}')

        # Fetch API data from baked URL and make sure we got the all the keys we need
        # We trust the API and assume it's all good once we got the recenttracks key
        # and recenttracks.track is a list (there are no tracks if its a dict)
        try:
            apiData = self._fetchAPIData(url)
            apiData = json.loads(apiData)

            if not apiData.get('recenttracks'):
                raise KeyError('Missing key: recenttracks')

            if not isinstance(apiData['recenttracks']['track'], list):
                return

        except json.JSONDecodeError as e:
            print(f'Error while decoding API data: {e}')
            return
        except KeyError as e:
            print(f'Error while reading API data: {e}')
            return

        # Calculate total pages. The check for zero is necessary if the from parameter in the API URL is in the future
        totalPages = int(apiData['recenttracks']['@attr']['totalPages'])
        if totalPages <= 0:
            totalPages = 1

        con, cur = self.DB.connect()

        for track in apiData['recenttracks']['track']:
            if not track.get('date'):
                # silently skip "now playing" track since it's not sure yet if it will be skipped
                continue

            q = 'INSERT INTO trackslog (scrobbleHash, playedOnTime, artistName, trackName, albumName) VALUES (?, ?, ?, ?, ?);'
            v = [
                hashlib.sha256(f'{track["date"]["uts"]}{track["artist"]["#text"]}{track["name"]}{track["album"]["#text"]}'.lower().encode()).hexdigest(),
                track['date']['uts'],
                track['artist']['#text'],
                track['name'],
                track['album']['#text'] if track['album']['#text'] else None,
            ]
            try:
                cur.execute(q, v)
                print(f'+ {track["artist"]["#text"]} - {track["name"]}')
            except Exception as e:
                print(f'! {e} | {track["artist"]["#text"]} - {track["name"]}')

        con.commit()
        con.close()

        if page < totalPages:
            print(f': {totalPages - page} more {"pages" if totalPages - page > 1 else "page"}')
            time.sleep(self.conf['apiSubsequentPageRequestDelay'])
            self._fetchRecentTracks(page + 1)


    @staticmethod
    def _fetchAPIData(url: str) -> any:
        try:
            with urllib.request.urlopen(url) as f:
                return f.read()

        except urllib.error.URLError as e:
            print(f'URL error while fetching API data: {e}')

        except urllib.error.HTTPError as e:
            print(f'HTTP error while fetching API data: {e}')

        except Exception as e:
            print(f'Error while fetching API data: {e}')

        return ''
