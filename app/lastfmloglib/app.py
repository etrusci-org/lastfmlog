import os
import json
import urllib.request
import time
import datetime
import hashlib
import base64
import getpass

from .database import DatabaseSQLite
from .databaseschema import databaseSchema
from .databasequery import databaseQuery




class App:
    conf: dict
    args: dict

    localTimezoneOffset: int

    dataDir: str
    secretsFile: str
    databaseFile: str
    secrets: dict

    Database: DatabaseSQLite


    def __init__(self, conf: dict, args: dict) -> None:
        # 'member
        self.conf = conf
        self.args = args
        self.localTimezoneOffset = time.localtime().tm_gmtoff

        # Assume data directory path
        if args['datadir'] == None:
            self.dataDir = self.conf['dataDir']
        else:
            self.dataDir = args['datadir']

        # Assume secrets file path
        self.secretsFile = os.path.join(self.dataDir, 'secrets.dat')

        # Assume database file path
        self.databaseFile = os.path.join(self.dataDir, 'database.sqlite3')

        # Init database object
        self.Database = DatabaseSQLite(dbFile=self.databaseFile)

        # Check data dir path and stop the world from turning if it doesn exist
        if not os.path.isdir(self.dataDir):
            raise FileNotFoundError(f'Data directory not found: {self.dataDir}')

        # Check secrets file path and create the file if it does not exist yet
        if not os.path.isfile(self.secretsFile):
            self._createSecretsFile()

        # Check database file path and create the file if it does not exist yet
        if not os.path.isfile(self.databaseFile):
            self._createDatabaseFile()

        # Load secrets
        try:
            with open(self.secretsFile, 'rb') as file:
                secrets = file.read()
                secrets = base64.b64decode(secrets)
                self.secrets = json.loads(secrets)
        except Exception as e:
            raise Exception(f'Error while loading secrets file: {e}')

        # Database and secrets file are valid if we reach this line


    def whoami(self) -> None:
        self._printWhoami()


    def nowplaying(self) -> None:
        np = self._fetchNowPlayingTrack()

        if not self.args['json']:
            if not np['artist']:
                print('Silence')
            else:
                print(f'artist: {np["artist"]}')
                print(f' track: {np["track"]}')
                if np['album']:
                    print(f' album: {np["album"]}')
        else:
            npJSON = json.dumps(np, ensure_ascii=False, indent=4)
            print(npJSON)


    def update(self) -> None:
        con, cur = self.Database.connect()

        # Find the last playTime value so we can set the "from" and "to" parameter in the API URL accordingly.
        cur.execute('SELECT playTime FROM trackslog ORDER BY playTime DESC LIMIT 1;')
        dump = cur.fetchone()
        lastplayTime = dump[0] if dump else 0

        con.close()

        # Set the "from" and "to" parameters for the API URL if it's not set by the user
        if self.args['from'] == None:
            self.args['from'] = lastplayTime if self.args['to'] == None else 0

        if self.args['to'] == None or self.args['from'] >= self.args['to']:
            self.args['to'] = ''

        # Fetch tracks
        self._fetchRecentTracks()

        # Janitor
        self.Database.vacuum()


    def stats(self) -> None:
        self._createStatsFile()


    def resetDatabase(self) -> None:
        self._resetDatabase()
        self.Database.vacuum()


    def resetSecrets(self) -> None:
        self._resetSecrets()


    def _getStats(self) -> dict:
        con, cur = self.Database.connect()

        # Prepare stats data dict and add some useful extra information to it
        stats = {
            '_username': self.secrets['apiUser'],
            '_statsModifiedOn': int(time.time()),
            '_databaseModifiedOn': int(os.path.getmtime(self.databaseFile)),
            '_localTimezoneOffset': self.localTimezoneOffset,
            'playsTotal': 0,
            'plays7days': 0,
            'plays14days': 0,
            'plays30days': 0,
            'plays90days': 0,
            'plays180days': 0,
            'plays365days': 0,
            'uniqueArtists': 0,
            'uniqueTracks': 0,
            'uniqueAlbums': 0,
            'topArtists': [],
            'topTracks': [],
            'topAlbums': [],
            'playsByYear': [],
            'playsByMonth': [],
            'playsByDay': [],
            'playsByHour': [],
        }

        # Total plays
        cur.execute(databaseQuery['playsTotal'])
        stats['playsTotal'] = cur.fetchone()[0]

        # Plays 7 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 7)),
        })
        plays = cur.fetchone()[0]
        stats['plays7days'] = {
            'plays': plays,
            'average': int(plays / 7)
        }

        # Plays 14 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 14)),
        })
        plays = cur.fetchone()[0]
        stats['plays14days'] = {
            'plays': plays,
            'average': int(plays / 14)
        }

        # Plays 30 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 30)),
        })
        plays = cur.fetchone()[0]
        stats['plays30days'] = {
            'plays': plays,
            'average': int(plays / 30)
        }

        # Plays 90 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 90)),
        })
        plays = cur.fetchone()[0]
        stats['plays90days'] = {
            'plays': plays,
            'average': int(plays / 90)
        }

        # Plays 180 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 180)),
        })
        plays = cur.fetchone()[0]
        stats['plays180days'] = {
            'plays': plays,
            'average': int(plays / 180)
        }

        # Plays 365 days
        cur.execute('SELECT COUNT(playHash) FROM trackslog WHERE playTime >= :time ORDER BY playTime DESC;', {
            'time': int(time.time() - (86400 * 365)),
        })
        plays = cur.fetchone()[0]
        stats['plays365days'] = {
            'plays': plays,
            'average': int(plays / 365)
        }

        # Unique artists
        cur.execute(databaseQuery['uniqueArtists'])
        stats['uniqueArtists'] = cur.fetchone()[0]

        # Unique tracks
        cur.execute(databaseQuery['uniqueTracks'])
        stats['uniqueTracks'] = cur.fetchone()[0]

        # Unique albums
        cur.execute(databaseQuery['uniqueAlbums'])
        stats['uniqueAlbums'] = cur.fetchone()[0]

        # Top artists
        cur.execute(databaseQuery['topArtists'], {
            'limit': self.args['limittopartists'] if self.args['limittopartists'] else stats['uniqueArtists'],
        })
        for row in cur:
            stats['topArtists'].append({
                'plays': row[1],
                'artist': row[0],
            })

        # Top tracks
        cur.execute(databaseQuery['topTracks'], {
            'limit': self.args['limittoptracks'] if self.args['limittoptracks'] else stats['uniqueTracks'],
        })
        for row in cur:
            stats['topTracks'].append({
                'plays': row[2],
                'artist': row[0],
                'track': row[1],
            })

        # Top albums
        cur.execute(databaseQuery['topAlbums'], {
            'limit': self.args['limittopalbums'] if self.args['limittopalbums'] else stats['uniqueAlbums'],
        })
        for row in cur:
            stats['topAlbums'].append({
                'plays': row[2],
                'artist': row[0],
                'album': row[1],
            })

        # Plays by year
        cur.execute(databaseQuery['playsByYear'], {
            'limit': self.args['limitplaysbyyear'] if self.args['limitplaysbyyear'] else stats['playsTotal'],
        })
        for row in cur:
            stats['playsByYear'].append({
                'plays': row[1],
                'year': row[0],
            })

        # Plays by month
        cur.execute(databaseQuery['playsByMonth'], {
            'limit': self.args['limitplaysbymonth'] if self.args['limitplaysbymonth'] else stats['playsTotal'],
        })
        for row in cur:
            month = self._convertDatetimeStringToLocalTimezone(f'{row[0]}-01 00:00:00')[0:7]
            stats['playsByMonth'].append({
                'plays': row[1],
                'month': month,
            })

        # Plays by day
        cur.execute(databaseQuery['playsByDay'], {
            'limit': self.args['limitplaysbyday'] if self.args['limitplaysbyday'] else stats['playsTotal'],
        })
        for row in cur:
            day = self._convertDatetimeStringToLocalTimezone(f'{row[0]} 00:00:00')[0:10]
            stats['playsByDay'].append({
                'plays': row[1],
                'day': day,
            })

        # Plays by hour
        cur.execute(databaseQuery['playsByHour'], {
            'limit': self.args['limitplaysbyhour'] if self.args['limitplaysbyhour'] else stats['playsTotal'],
        })
        for row in cur:
            hour = self._convertDatetimeStringToLocalTimezone(f'{row[0]}:00:00')
            stats['playsByHour'].append({
                'plays': row[1],
                'hour': hour[0:13],
            })

        # Don't need the database anymore
        con.close()

        return stats


    def _createStatsFile(self) -> None:
        print(f'Creating stats file')

        stats = self._getStats()
        statsFile = os.path.join(self.dataDir, 'stats.json')

        with open(statsFile, mode='w') as file:
            file.write(json.dumps(stats, ensure_ascii=False, indent=4))


    def _fetchRecentTracks(self, page: int = 1, _addedTracks: int = 0) -> None:
        # Bake API URL
        apiURL = self.conf['apiBaseURL']
        apiURL += '?method=user.getrecenttracks'
        apiURL += '&format=json'
        apiURL += '&extended=1'
        apiURL += f'&limit={self.conf["apiRequestLimitInitial"] if self.args["from"] == 0 or time.time() - self.args["from"] > self.conf["apiRequestSwitchToInitialLimitTreshold"] else self.conf["apiRequestLimitIncremental"]}'
        apiURL += f'&from={self.args["from"]}'
        apiURL += f'&to={self.args["to"]}'
        apiURL += f'&page={page}'
        apiURL += f'&user={self.secrets["apiUser"]}'
        apiURL += f'&api_key={self.secrets["apiKey"]}'

        # Fetch API data from URL
        print(f'Fetching API data page {page}')
        apiData = self._fetchJSONAPIData(apiURL)

        # Check if we got the stuff we need in apiData or stop
        if not apiData.get('recenttracks'):
            raise KeyError('Missing "recenttracks" key')

        if not isinstance(apiData['recenttracks']['track'], list):
            raise TypeError('Incorrect track list type')

        # Calculate total pages
        # The check for zero is necessary if the from parameter in the API URL is in the future
        totalPages = int(apiData['recenttracks']['@attr']['totalPages'])
        if totalPages <= 0:
            totalPages = 1

        # Insert fetched API data into database
        con, cur = self.Database.connect()

        try:
            for track in apiData['recenttracks']['track']:
                # silently skip currently playing track
                if not track.get('date'):
                    continue

                cur.execute(databaseQuery['trackslogInsertNewTrack'], {
                    'playHash': self._getPlayHash(track),
                    'playTime': track['date']['uts'],
                    'artist': track['artist']['name'],
                    'track': track['name'],
                    'album': track['album']['#text'] if track['album']['#text'] else None,
                })

                _addedTracks += 1

                if self.args['verbose']:
                    print(f'+ {track["artist"]["name"]} - {track["name"]}')

        except Exception as e:
            if str(e).lower().find('unique') == -1:
                print(f'! {track["artist"]["name"]} - {track["name"]} | {e}')

        finally:
            con.commit()
            con.close()

        # Fetch the next data page if there is one
        if page < totalPages:
            print(f'{totalPages - page} more {"pages" if totalPages - page > 1 else "page"} to fetch')
            time.sleep(self.conf['apiRequestPagingDelay'])
            self._fetchRecentTracks(page=page + 1, _addedTracks=_addedTracks)
            return

        print(f'Added {_addedTracks} {"tracks" if _addedTracks == 0 or _addedTracks > 1 else "track"}')


    def _fetchNowPlayingTrack(self) -> dict:
        # Bake API URL
        apiURL = self.conf['apiBaseURL']
        apiURL += '?method=user.getrecenttracks'
        apiURL += '&format=json'
        apiURL += '&extended=1'
        apiURL += f'&limit=1'
        apiURL += f'&user={self.secrets["apiUser"]}'
        apiURL += f'&api_key={self.secrets["apiKey"]}'

        # Fetch API data from URL
        apiData = self._fetchJSONAPIData(apiURL)

        np = {
            'artist': None,
            'track': None,
            'album': None,
        }

        # Check if we got the stuff we need in apiData or stop
        if not apiData.get('recenttracks'):
            raise KeyError('Missing "recenttracks" key')

        if not isinstance(apiData['recenttracks']['track'], list):
            raise TypeError('Incorrect track list type')

        if not apiData['recenttracks']['track'][0].get('@attr'):
            return np

        if not apiData['recenttracks']['track'][0]['@attr'].get('nowplaying'):
            return np

        # Return now playing track info
        track = apiData['recenttracks']['track'][0]

        if track['@attr']['nowplaying'] == 'true':
            np['artist'] = track["artist"]["name"]
            np['track'] = track["name"]
            np['album'] = track["album"]["#text"] if track["album"]["#text"] else None

        return np


    def _createSecretsFile(self) -> None:
        print(f'Creating secrets file')
        print('See the README on how to get your API credentials. <https://github.com/etrusci-org/lastfmlog#readme>', end='\n\n')

        while True:
            apiUser = input('Enter your Last.fm username: ').strip()
            apiKey = getpass.getpass('Enter your Last.fm API key (input will be hidden): ').strip()

            if not apiUser or not apiKey:
                print('You must enter both username and API key.')
            else:
                break

        print()

        secrets = json.dumps({'apiUser': apiUser, 'apiKey': apiKey}, ensure_ascii=False, indent=4)

        with open(self.secretsFile, 'wb') as file:
            secrets = base64.b64encode(secrets.encode())
            file.write(secrets)


    def _createDatabaseFile(self) -> None:
        print(f'Creating database file')

        con, cur = self.Database.connect()

        try:
            cur.executescript(databaseSchema)
        except Exception:
            os.unlink(self.databaseFile)
            raise
        finally:
            con.close()
            print()


    def _resetDatabase(self) -> None:
        con, cur = self.Database.connect()

        try:
            cur.executescript(databaseQuery['resetDatabase'])
            print(f'Database reset')
        except Exception as e:
            print(f'Could not reset database: {e}')
        finally:
            con.close()


    def _resetSecrets(self) -> None:
        print('Deleting secrets file')
        secretsFile = os.path.join(self.dataDir, 'secrets.dat')
        os.unlink(secretsFile)


    def _printWhoami(self) -> None:
        whoami = self._getWhoami()
        print(f'      username: {whoami["user"]["name"]}')
        print(f' registered on: {datetime.datetime.utcfromtimestamp(int(whoami["user"]["registered"]["unixtime"]))} UTC')
        print(f'         plays: {whoami["user"]["playcount"]}')
        print(f'       artists: {whoami["user"]["artist_count"]}')
        print(f'        tracks: {whoami["user"]["track_count"]}')
        print(f'        albums: {whoami["user"]["album_count"]}')


    def _getWhoami(self) -> dict:
        return self._fetchJSONAPIData(url=f'{self.conf["apiBaseURL"]}?method=user.getinfo&format=json&user={self.secrets["apiUser"]}&api_key={self.secrets["apiKey"]}')


    def _convertDatetimeStringToLocalTimezone(self, datetime: str) -> str:
        unixTimestamp = time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S'))
        localTimestamp = unixTimestamp + self.localTimezoneOffset
        localDatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(localTimestamp))
        return localDatetime


    def _fetchJSONAPIData(self, url: str) -> dict:
        try:
            if not url.lower().startswith(self.conf['apiBaseURL']):
                raise ValueError(f'Invalid API URL. Must start with: {self.conf["apiBaseURL"]}')

            with urllib.request.urlopen(url) as response: # nosec B310
                return json.load(response)

        except Exception as e:
            raise Exception(f'Error while fetching API data: {e}')


    @staticmethod
    def _getPlayHash(track: dict) -> str:
        raw = str(track['date']['uts'] + track['artist']['name'] + track['name'] + track['album']['#text']).lower()
        return hashlib.sha256(raw.encode()).hexdigest()


    # TODO: clean local database method
    #
    # Cleans tracks in local database which are not existing in the remote API data anymore
    #
    # 1. get all remote tracks list
    # 2. get all local tracks list
    # 3. delete all local tracks that are not in the remote tracks list
    # 4. profit?
