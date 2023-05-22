import os
import json
import urllib.request
import time
import datetime
import hashlib

from .database import DatabaseSQLite
from .databaseschema import databaseSchema
from .databasequery import databaseQuery




class App:
    conf: dict
    args: dict

    timezoneOffset: int

    dataDir: str
    secretsFile: str
    databaseFile: str
    secrets: dict

    Database: DatabaseSQLite


    def __init__(self, conf: dict, args: dict) -> None:
        # 'member
        self.conf = conf
        self.args = args
        self.timezoneOffset = time.localtime().tm_gmtoff

        # Assume data directory path
        if args['datadir'] == None:
            self.dataDir = self.conf['dataDir']
        else:
            self.dataDir = args['datadir']

        # Assume secrets file path
        self.secretsFile = os.path.join(self.dataDir, 'secrets.json')

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
            with open(self.secretsFile) as file:
                self.secrets = json.load(file)
        except json.JSONDecodeError as e:
            raise SyntaxError(f'Synatx error in secrets file: {e}')

        # Database and secrets file are valid if we reach this line


    def whoami(self) -> None:
        self._printWhoami()


    def update(self) -> None:
        con, cur = self.Database.connect()

        # Find the last playTime value so we can set the from parameter in the API URL accordingly.
        cur.execute('SELECT playTime FROM trackslog ORDER BY playTime DESC LIMIT 1;')
        dump = cur.fetchone()
        lastplayTime = dump[0] if dump else 0

        con.close()

        # Set the from and to parameters for the API URL if it's not set by the user
        if self.args["from"] == None:
            self.args["from"] = lastplayTime if self.args['to'] == None else 0

        if self.args["to"] == None:
            self.args["to"] = ''

        # Fetch tracks
        self._fetchRecentTracks()

        # Janitor
        self.Database.vacuum()


    def stats(self) -> None:
        self._createStatsFile()


    def _createStatsFile(self) -> None:
        con, cur = self.Database.connect()

        # Prepare stats data dict and add some useful extra information to it
        stats = {
            '_statsModifiedOn': int(time.time()),
            '_databaseModifiedOn': int(os.path.getmtime(self.databaseFile)),
            '_timezoneOffset': self.timezoneOffset,
            'totalPlays': 0,
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
        cur.execute(databaseQuery['totalPlays'])
        stats['totalPlays'] = cur.fetchone()[0]

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
            'limit': 10,
        })
        for row in cur:
            stats['topArtists'].append({
                'plays': row[1],
                'artist': row[0],
            })

        # Top tracks
        cur.execute(databaseQuery['topTracks'], {
            'limit': 10,
        })
        for row in cur:
            stats['topTracks'].append({
                'plays': row[2],
                'artist': row[0],
                'track': row[1],
            })

        # Top albums
        cur.execute(databaseQuery['topAlbums'], {
            'limit': 10,
        })
        for row in cur:
            stats['topAlbums'].append({
                'plays': row[2],
                'artist': row[0],
                'album': row[1],
            })

        # Plays by year
        cur.execute(databaseQuery['playsByYear'], {
            'limit': 10,
        })
        for row in cur:
            stats['playsByYear'].append({
                'plays': row[1],
                'year': row[0],
            })

        # Plays by month
        cur.execute(databaseQuery['playsByMonth'], {
            'limit': 10,
        })
        for row in cur:
            month = self._convertDatetimeStringToLocalTimezone(f'{row[0]}-01 00:00:00')[0:7]
            stats['playsByMonth'].append({
                'plays': row[1],
                'month': month,
            })

        # Plays by day
        cur.execute(databaseQuery['playsByDay'], {
            'limit': 10,
        })
        for row in cur:
            day = self._convertDatetimeStringToLocalTimezone(f'{row[0]} 00:00:00')[0:10]
            stats['playsByDay'].append({
                'plays': row[1],
                'day': day,
            })

        # Plays by hour
        cur.execute(databaseQuery['playsByHour'], {
            'limit': 10,
        })
        for row in cur:
            dump = self._convertDatetimeStringToLocalTimezone(f'{row[0]}:00:00')
            hour = dump[11:13]
            day = dump[0:10]
            stats['playsByHour'].append({
                'plays': row[1],
                'hour': hour,
                'day': day,
            })

        # Don't need the database anymore
        con.close()

        # Finally save the stats file
        statsFile = os.path.join(self.dataDir, 'stats.json')
        with open(statsFile, mode='w') as file:
            file.write(json.dumps(stats, ensure_ascii=False, indent=4))
            print(f'Stats saved to file: {statsFile}')


    def reset(self) -> None:
        self._resetDatabase()
        self.Database.vacuum()


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
        else:
            print(f'Added {_addedTracks} {"tracks" if _addedTracks == 0 or _addedTracks > 1 else "track"}')


    def _createSecretsFile(self) -> None:
        print(f'Creating secrets file: {self.secretsFile}')
        print('No worries if you make mistakes, you can edit the file in a text editor.')
        print('See the README on how to get an API key.')

        secrets = self.conf['secretsTemplate']
        secrets['apiUser'] = input('Enter your Last.fm username: ').strip()
        secrets['apiKey'] = input('Enter your Last.fm API key: ').strip()

        with open(self.secretsFile, 'x') as file:
            json.dump(obj=secrets, fp=file, indent=4)


    def _createDatabaseFile(self) -> None:
        print(f'Creating database file: {self.databaseFile}')

        con, cur = self.Database.connect()

        try:
            cur.executescript(databaseSchema)
        except Exception:
            os.unlink(self.databaseFile)
            raise
        finally:
            con.close()


    def _resetDatabase(self) -> None:
        con, cur = self.Database.connect()

        try:
            cur.executescript(databaseQuery['resetDatabase'])
            print(f'Database reset')
        except Exception as e:
            print(f'Could not reset database: {e}')
        finally:
            con.close()


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
        localTimestamp = unixTimestamp + self.timezoneOffset
        localDatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(localTimestamp))
        return localDatetime


    @staticmethod
    def _fetchJSONAPIData(url: str) -> dict:
        try:
            with urllib.request.urlopen(url) as response:
                return json.load(response)

        except Exception as e:
            raise Exception(f'Error while fetching API data: {e}')


    @staticmethod
    def _getPlayHash(track: dict) -> str:
        raw = str(track["date"]["uts"] + track["artist"]["name"] + track["name"] + track["album"]["#text"]).lower()
        return hashlib.sha256(raw.encode()).hexdigest()