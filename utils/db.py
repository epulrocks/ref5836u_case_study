import sqlite3
from pathlib import Path
from pandas import read_sql_query

class ReferenceDB:
    def __init__(self, db_path: Path):
        self.db_path = db_path.absolute()
        self.con = sqlite3.connect(self.db_path)
    def query(self, sql_query: str):
        return read_sql_query(sql_query, self.con)
    def close(self):
        if self.con:
            self.con.close()