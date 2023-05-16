import os
import json
import urllib.request
import hashlib
import time

from .db import DatabaseSQLite




class Core:
    conf: dict
    args: dict

    dataDir: str
    secretsFile: str
    dbFile: str

    DB: DatabaseSQLite

    RAM: dict = {
        'lastPlayedOnTime': -1,
    }


    def __init__(self, conf: dict, args: dict) -> None:
        # 'member
        self.conf = conf
        self.args = args

        # Assume crucial paths and check them
        self.dataDir = args['datadir'] if args['datadir'] else conf['defaultDataDir']
        self.secretsFile = os.path.join(self.dataDir, conf['secretsFileName'])
        try:
            if not os.path.isdir(self.dataDir):
                raise FileNotFoundError(f'Invalid data directory path: {self.dataDir}')
            if not os.path.isfile(self.secretsFile):
                raise FileNotFoundError(f'Invalid secrets file path: {self.secretsFile}')
        except FileNotFoundError as e:
            print(e)
            exit(1)

        # Load secrets
        try:
            with open(self.secretsFile) as f:
                self.secrets = json.load(f)
        except json.JSONDecodeError as e:
            print(f'Error while decoding secrets file: {e}')
            exit(1)

        # Data dir and secrets file are ok if we reach this line,
        # therefore we can now create the database file if it does not exist already
        self.dbFile = os.path.join(self.dataDir, conf['dbFileName'])
        self.DB = DatabaseSQLite(dbFile=self.dbFile)
        if not os.path.isfile(self.dbFile):
            self._createDatabase()


    def update(self) -> None:
        if not self.args['updatefromstart']:
            self.RAM['lastPlayedOnTime'] = self._getLastPlayedOnTime()

        self._fetchRecentTracks()

        self.DB.vacuum()


    def _getLastPlayedOnTime(self) -> int:
        con, cur = self.DB.connect()
        q = 'SELECT playedOnTime FROM trackslog LIMIT 1;'
        cur.execute(q)
        dump = cur.fetchone()
        con.close()
        return dump[0] if dump else self.RAM['lastPlayedOnTime']


    def _fetchRecentTracks(self, page: int = 1, _newTracksCount: int = 0, _skippedTracksCount: int = 0) -> None:
        # Bake API url
        url  = self.conf['api']['baseURL']
        url += '?method=user.getrecenttracks'
        url += '&format=json'
        url += '&extended=0'
        url += f'&limit={self.conf["api"]["itemsPerPageLimitInitial"] if self.RAM["lastPlayedOnTime"] == -1 else self.conf["api"]["itemsPerPageLimitIncremental"]}'
        url += f'&from={self.RAM["lastPlayedOnTime"] + 1}'
        url += f'&page={page}'
        url += f'&user={self.secrets["apiUser"]}'
        url += f'&api_key={self.secrets["apiKey"]}'

        print(f'Fetching data page {page}')

        # Fetch API data from baked URL and make sure we got the all the keys we need
        # We trust the API and assume it's all good once we got the recenttracks key
        # and recenttracks.track is a list (there are no tracks if its a dict)
        try:
            apiData = self._fetchAPIData(url)
            apiData = json.loads(apiData)

            if not apiData.get('recenttracks'):
                raise KeyError('Missing key: recenttracks')

            if not isinstance(apiData['recenttracks']['track'], list):
                print('no new tracks to fetch')
                return

        except json.JSONDecodeError as e:
            print(f'Error while decoding API data: {e}')
            return
        except KeyError as e:
            print(f'Error while parsing API data: {e}')
            return

        # Calculate total pages.
        # The check for zero is necessary if the from parameter in the API URL is in the future
        totalPages = int(apiData['recenttracks']['@attr']['totalPages'])
        if totalPages <= 0:
            totalPages = 1

        con, cur = self.DB.connect()

        # Store tracks in database
        for track in apiData['recenttracks']['track']:
            # silently skip currently playing track
            if not track.get('date'):
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
                _newTracksCount += 1
            except Exception as e:
                if str(e).find('UNIQUE') != -1:
                    print(f'~ {track["artist"]["#text"]} - {track["name"]}')
                else:
                    print(f'! {e} | {track["artist"]["#text"]} - {track["name"]}')

        con.commit()
        con.close()

        # Fetch the next data page if there is one
        if page < totalPages:
            print(f'{totalPages - page} more {"pages" if totalPages - page > 1 else "page"} to fetch')
            time.sleep(self.conf['api']['subsequentPageRequestDelay'])
            self._fetchRecentTracks(page + 1, _newTracksCount, _skippedTracksCount)

        print(f'Fetched {_newTracksCount} new {"tracks" if _newTracksCount == 0 or _newTracksCount > 1 else "track"}')
        print(f'Skipped {_skippedTracksCount} {"tracks" if _skippedTracksCount == 0 or _skippedTracksCount > 1 else "track"}')


    def _createDatabase(self) -> None:
        con, cur = self.DB.connect()
        try:
            cur.executescript(self.conf['dbSchema'])
        except Exception as e:
            print(f'Error while creating database: {e}')
            os.unlink(self.dbFile)
        finally:
            con.close()


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
