import os
import json
import urllib.request
import hashlib
import time

from .db import DatabaseSQLite
from .query import query




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


    def stats(self) -> None:
        con, cur = self.DB.connect()

        # 'member stuff for later use
        cur.execute(query['trackslogRowCount'])
        trackslogRowCount = cur.fetchone()[0]
        dbMtime = os.path.getmtime(self.dbFile)
        dbAge = time.time() - dbMtime
        defaultQueryLimit = trackslogRowCount

        print(f'Local database has {trackslogRowCount} {"tracks" if trackslogRowCount == 0 or trackslogRowCount > 1 else "tracks"} stored and was changed {round(dbAge / 60)}m ago')

        # Check for empty or outdated database
        if self.args['obsoleteafter'] > 0:
            if trackslogRowCount <= 0 or dbAge > self.args['obsoleteafter']:
                x = input('Update database first? [Y/n]: ').strip().lower()
                if x == '' or x == 'y':
                    self.update()

        stats = {
            '_statsUpdatedOn': time.time(),
            '_databaseUpdatedOn': dbMtime,
            '_defaultQueryLimit': defaultQueryLimit,
            'playsTotal': trackslogRowCount,
            'uniqueArtists': None,
            'uniqueTracks': None,
            'uniqueAlbums': None,
            'topArtists': [],
            'topTracks': [],
            'topAlbums': [],
            'playsByYear': [],
            'playsByMonth': [],
            'playsByDay': [],
            'playsByHour': [],
        }

        # unique artists
        cur.execute(query['uniqueArtists'])
        stats['uniqueArtists'] = cur.fetchone()[0]

        # unique tracks
        cur.execute(query['uniqueTracks'])
        stats['uniqueTracks'] = cur.fetchone()[0]

        # unique albums
        cur.execute(query['uniqueAlbums'])
        stats['uniqueAlbums'] = cur.fetchone()[0]

        # top artists
        cur.execute(query['topArtists'], {'limit': self.args['topartistslimit'] if self.args['topartistslimit'] else defaultQueryLimit})
        for v in cur:
            stats['topArtists'].append({
                'artist': v[0],
                'plays': v[1],
            })

        # top tracks
        cur.execute(query['topTracks'], {'limit': self.args['toptrackslimit'] if self.args['toptrackslimit'] else defaultQueryLimit})
        for v in cur:
            stats['topTracks'].append({
                'track': v[1],
                'artist': v[0],
                'plays': v[2],
            })

        # top albums
        cur.execute(query['topAlbums'], {'limit': self.args['topalbumslimit'] if self.args['topalbumslimit'] else defaultQueryLimit})
        for v in cur:
            stats['topAlbums'].append({
                'album': v[1],
                'artist': v[0],
                'plays': v[2],
            })

        # plays by year
        cur.execute(query['playsByYear'], {'limit': self.args['playsbyyearlimit'] if self.args['playsbyyearlimit'] else defaultQueryLimit})
        for v in cur:
            stats['playsByYear'].append({
                'year': v[0],
                'plays': v[1],
            })

        # plays by month
        cur.execute(query['playsByMonth'], {'limit': self.args['playsbymonthlimit'] if self.args['playsbymonthlimit'] else defaultQueryLimit})
        for v in cur:
            stats['playsByMonth'].append({
                'month': v[0],
                'plays': v[1],
            })

        # plays by day
        cur.execute(query['playsByDay'], {'limit': self.args['playsbydaylimit'] if self.args['playsbydaylimit'] else defaultQueryLimit})
        for v in cur:
            stats['playsByDay'].append({
                'day': v[0],
                'plays': v[1],
            })

        # plays by Hour
        cur.execute(query['playsByHour'], {'limit': self.args['playsbyhourlimit'] if self.args['playsbyhourlimit'] else defaultQueryLimit})
        for v in cur:
            stats['playsByHour'].append({
                'hour': v[0].split(' ')[1],
                'day': v[0].split(' ')[0],
                'plays': v[1],
            })

        # Done querying the database
        con.close()

        # Save the stats to a file
        statsFile = os.path.join(self.dataDir, self.conf['statsFileName'])
        with open(statsFile, mode='w') as f:
            f.write(json.dumps(stats, ensure_ascii=False, indent=4))
            print(f'Stats saved to file: {statsFile}')


    def reset(self) -> None:
        x = input('Reset database? [Y/n]: ').strip().lower()
        if x != 'y':
            return

        con, cur = self.DB.connect()
        q = 'DELETE FROM trackslog;'
        cur.execute(q)
        print(f'Deleted {cur.rowcount} {"tracks" if cur.rowcount == 0 or cur.rowcount > 1 else "tracks"}')
        con.commit()
        con.close()

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

        # Store tracks in database
        try:
            con, cur = self.DB.connect()
            for track in apiData['recenttracks']['track']:
                # silently skip currently playing track
                if not track.get('date'):
                    continue
                q = 'INSERT INTO trackslog (scrobbleHash, playedOnTime, artistName, trackName, albumName) VALUES (:scrobbleHash, :playedOnTime, :artistName, :trackName, :albumName);'
                v = {
                    'scrobbleHash': hashlib.sha256(f'{track["date"]["uts"]}{track["artist"]["#text"]}{track["name"]}{track["album"]["#text"]}'.lower().encode()).hexdigest(),
                    'playedOnTime': track['date']['uts'],
                    'artistName': track['artist']['#text'],
                    'trackName': track['name'],
                    'albumName': track['album']['#text'] if track['album']['#text'] else None,
                }
                cur.execute(q, v)
                print(f'+ {track["artist"]["#text"]} - {track["name"]}')
                _newTracksCount += 1
        except Exception as e:
            if str(e).find('UNIQUE') != -1:
                print(f'~ {track["artist"]["#text"]} - {track["name"]}')
            else:
                print(f'! {e} | {track["artist"]["#text"]} - {track["name"]}')
            _skippedTracksCount += 1
        finally:
            con.commit()
            con.close()

        # Fetch the next data page if there is one
        if page < totalPages:
            print(f'{totalPages - page} more {"pages" if totalPages - page > 1 else "page"} to fetch')
            time.sleep(self.conf['api']['subsequentPageRequestDelay'])
            self._fetchRecentTracks(page + 1, _newTracksCount, _skippedTracksCount)
        else:
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
