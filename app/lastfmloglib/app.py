import os
import json
import typing
import urllib.request
import time
import datetime
import hashlib
import base64
import getpass

from .log import Logger
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

    Log: Logger
    Database: DatabaseSQLite


    def __init__(self, conf: dict, args: dict, Log: Logger) -> None:
        # 'member
        self.conf = conf
        self.args = args
        self.Log = Log
        self.localTimezoneOffset = time.localtime().tm_gmtoff

        # Assume data directory path
        if not args['datadir']:
            self.dataDir = self.conf['dataDir']
        else:
            self.dataDir = args['datadir']

        # Assume secrets file path
        self.secretsFile = os.path.join(self.dataDir, self.conf['secretsFilename'])

        # Assume database file path
        self.databaseFile = os.path.join(self.dataDir, self.conf['databaseFilename'])

        # Init database object
        self.Database = DatabaseSQLite(dbFile=self.databaseFile)

        # Check data dir path and stop the world from turning if it does not exist
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


    def executeAction(self, action: str) -> None:
        if action not in self.conf['actionArgs']:
            raise ValueError(f'Invalid action')

        if action == 'whoami':
            self._printWhoami()

        if action == 'update':
            self._updateDatabase()

        if action == 'stats':
            self._createStatsFile()

        if action == 'nowplaying':
            self._printNowPlayingTrack()

        if action == 'trimdatabase':
            self._trimDatabase()

        if action == 'resetdatabase':
            self._resetDatabase()

        if action == 'resetsecrets':
            self._resetSecrets()

        if action == 'export':
            self._createExportFile()


    def _updateDatabase(self) -> None:
        con, cur = self.Database.connect()

        # Find the last playTime value so we can set the "from" and "to" parameter in the API URL accordingly.
        cur.execute('SELECT playTime FROM trackslog ORDER BY playTime DESC LIMIT 1;')
        dump = cur.fetchone()
        lastPlayTime = dump[0] if dump else 0
        con.close()

        # Set the "from" and "to" parameters for the API URL if it's not set by the user
        if self.args['from'] == None:
            self.args['from'] = lastPlayTime if self.args['to'] == None else 0

        if self.args['to'] == None or self.args['from'] >= self.args['to']:
            self.args['to'] = ''

        # Fetch tracks
        self._fetchRecentTracks()


    def _createExportFile(self) -> None:
        self.Log.msg('exporting database source code')

        outputFile = os.path.join(self.dataDir, f'{self.conf["exportFilename"]}')

        con, _ = self.Database.connect()

        with open(outputFile, 'w') as file:
            for row in con.iterdump():
                file.write(f'{row}\n')

        con.close()

        self.Log.msg(f'wrote {os.path.getsize(outputFile)} bytes to {self.conf["exportFilename"]}')


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
        self.Log.msg('loading statistics data')
        stats = self._getStats()

        statsFile = os.path.join(self.dataDir, self.conf['statsFilename'])
        statsData = json.dumps(stats, ensure_ascii=False, indent=4)

        with open(statsFile, mode='w') as file:
            file.write(statsData)

        self.Log.msg(f'wrote {os.path.getsize(statsFile)} bytes to {self.conf["statsFilename"]}')


    def _fetchRecentTracks(self, page: int = 1, _addedTracks: int = 0) -> None:
        # Bake API URL
        limitParamValue = self.conf["apiRequestLimitInitial"] if self.args["from"] == 0 or time.time() - self.args["from"] > self.conf["apiRequestSwitchToInitialLimitTreshold"] else self.conf["apiRequestLimitIncremental"]

        apiURL = self.conf['apiBaseURL']
        apiURL += '?method=user.getrecenttracks'
        apiURL += '&format=json'
        apiURL += '&extended=1'
        apiURL += f'&limit={limitParamValue}'
        apiURL += f'&from={self.args["from"]}'
        apiURL += f'&to={self.args["to"]}'
        apiURL += f'&page={page}'
        apiURL += f'&user={self.secrets["apiUser"]}'
        apiURL += f'&api_key={self.secrets["apiKey"]}'

        # Fetch API data from URL
        self.Log.msg(f'downloading page:{page}', end=' ' if page == 1 else '\n')
        if page == 1:
            self.Log.msg(f'from:{self.args["from"]} to:{self.args["to"] or "latest"} limit:{limitParamValue}')

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

        except Exception as e:
            if str(e).lower().find('unique') == -1:
                self.Log.msg(f'! {track["artist"]["name"]} - {track["name"]} | {e}')

        finally:
            con.commit()
            con.close()

        # Fetch the next data page if there is one
        if page < totalPages:
            self.Log.msg(f'{totalPages - page} more {"pages" if totalPages - page > 1 else "page"}')
            time.sleep(self.conf['apiRequestPagingDelay'])
            self._fetchRecentTracks(page=page + 1, _addedTracks=_addedTracks)
            return

        self.Log.msg(f'added {_addedTracks} {"tracks" if _addedTracks == 0 or _addedTracks > 1 else "track"}')
        if _addedTracks > 0:
            self.Database.vacuum()


    def _trimDatabase(self) -> None:
        # Get all remote tracks
        self.Log.msg('loading remote tracks')

        trimhashesFile = os.path.join(self.dataDir, 'tmp-trim-hashes.txt')
        trimtaFile = os.path.join(self.dataDir, 'tmp-trim-transaction.txt')

        with open(trimhashesFile, 'w') as file:
            for playHash in self._fetchRecentTracksAll():
                file.write(f'{playHash}\n')

        # Delete all local tracks that are not in the remote tracks list
        self.Log.msg('baking transaction source code')

        con, cur = self.Database.connect()
        cur.execute('SELECT playHash, artist, track FROM trackslog;')

        _trimmedTracks = 0

        with open(trimhashesFile, 'r') as hashesFile, open(trimtaFile, 'w+') as taFile:
            taFile.write('BEGIN;\n')

            for row in cur:
                if not self._stringInFileLine(row[0], hashesFile):
                    taFile.write(f'DELETE FROM trackslog WHERE playHash = \'{row[0]}\';\n') # nosec B608
                    _trimmedTracks += 1

            taFile.write('COMMIT;\n')

            self.Log.msg('trimming trackslog table')
            taFile.seek(0)
            cur.executescript(taFile.read())

        con.close()

        self.Log.msg(f'deleted {_trimmedTracks} {"tracks" if _trimmedTracks == 0 or _trimmedTracks > 1 else "track"}')
        if _trimmedTracks > 0:
            self.Database.vacuum()


    def _fetchRecentTracksAll(self, page: int = 1) -> str:
        # Bake API URL
        apiURL = self.conf['apiBaseURL']
        apiURL += '?method=user.getrecenttracks'
        apiURL += '&format=json'
        apiURL += '&extended=1'
        apiURL += f'&limit={self.conf["apiRequestLimitInitial"]}'
        apiURL += f'&from=0'
        apiURL += f'&page={page}'
        apiURL += f'&user={self.secrets["apiUser"]}'
        apiURL += f'&api_key={self.secrets["apiKey"]}'

        # Fetch API data from URL
        self.Log.msg(f'downloading page:{page}', end=' ' if page == 1 else '\n')
        if page == 1:
            self.Log.msg(f'from:0 to:latest limit:{self.conf["apiRequestLimitInitial"]}')

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

        # Yield fetched API data
        for track in apiData['recenttracks']['track']:
            # silently skip currently playing track
            if not track.get('date'):
                continue

            playHash = self._getPlayHash(track)

            yield playHash

        # Fetch the next data page if there is one
        if page < totalPages:
            self.Log.msg(f'{totalPages - page} more {"pages" if totalPages - page > 1 else "page"}')
            time.sleep(self.conf['apiRequestPagingDelay'])
            yield from self._fetchRecentTracksAll(page=page + 1)


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


    def _printNowPlayingTrack(self) -> None:
        np = self._fetchNowPlayingTrack()

        if not self.args['json']:
            if not np['artist']:
                self.Log.msg('Silence')
            else:
                self.Log.msg(f'artist: {np["artist"]}')
                self.Log.msg(f' track: {np["track"]}')
                if np['album']:
                    self.Log.msg(f' album: {np["album"]}')
        else:
            if not np['artist']:
                np = {'silence': True}

            np = json.dumps(np, ensure_ascii=False, indent=4)

            self.Log.msg(np)


    def _createSecretsFile(self) -> None:
        self.Log.msg(f'creating secrets file')
        self.Log.msg('see the README on how to get your API credentials. <https://github.com/etrusci-org/lastfmlog#readme>', end='\n\n')

        while True:
            apiUser = input('enter your Last.fm username: ').strip()
            apiKey = getpass.getpass('enter your Last.fm API key (input will be hidden): ').strip()

            if not apiUser or not apiKey:
                self.Log.msg('! both username and API key are required')
            else:
                break

        secrets = json.dumps({'apiUser': apiUser, 'apiKey': apiKey}, ensure_ascii=False, indent=4)
        secrets = base64.b64encode(secrets.encode())

        with open(self.secretsFile, 'wb') as file:
            file.write(secrets)


    def _createDatabaseFile(self) -> None:
        self.Log.msg(f'creating database file')

        con, cur = self.Database.connect()

        try:
            cur.executescript(databaseSchema)
        except Exception:
            os.unlink(self.databaseFile)
            raise
        finally:
            con.close()


    def _resetDatabase(self) -> None:
        self.Log.msg('deleting database file')
        os.unlink(self.databaseFile)

        self._createDatabaseFile()


    def _resetSecrets(self) -> None:
        self.Log.msg('deleting secrets file')
        os.unlink(self.secretsFile)

        self._createSecretsFile()


    def _printWhoami(self) -> None:
        whoami = self._getWhoami()
        self.Log.msg(f'      username: {whoami["user"]["name"]}')
        self.Log.msg(f' registered on: {datetime.datetime.utcfromtimestamp(int(whoami["user"]["registered"]["unixtime"]))} UTC')
        self.Log.msg(f'         plays: {whoami["user"]["playcount"]}')
        self.Log.msg(f'       artists: {whoami["user"]["artist_count"]}')
        self.Log.msg(f'        tracks: {whoami["user"]["track_count"]}')
        self.Log.msg(f'        albums: {whoami["user"]["album_count"]}')
        self.Log.msg(f'data directory: {self.dataDir}')


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
        raw = str(
            track['date']['uts']
            + track['artist']['name']
            + track['name']
            + track['album']['#text']
        ).lower()

        return hashlib.sha256(raw.encode()).hexdigest()


    @staticmethod
    def _stringInFileLine(string: str, file: typing.IO[str]) -> bool:
        file.seek(0)

        for line in file:
            if string == line.strip():
                return True

        return False
