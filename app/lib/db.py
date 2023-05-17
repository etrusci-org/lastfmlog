import sqlite3




class DatabaseSQLite:
    dbFile: str


    def __init__(self, dbFile: str) -> None:
        self.dbFile = dbFile


    def connect(self) -> tuple:
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        return (con, cur)


    def vacuum(self) -> None:
        con, cur = self.connect()
        cur.execute('VACUUM;')
        con.close()
