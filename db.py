from typing import List, Any, Dict
import sqlite3
from contextlib import contextmanager

from dirs import DATA_DIR


# SQLite doesn't have a native boolean type so we'll
# just implicitly convert them to integers.
sqlite3.register_adapter(bool, int)

DB_PATH = DATA_DIR / 'db.sqlite3'


class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(DB_PATH)

    @contextmanager
    def cursor(self):
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        finally:
            cur.close()

    def execute(self, sql: str):
        with self.cursor() as cur:
            cur.execute(sql)

    def drop_and_create_table(self, name: str, columns: Dict[str, str]) -> None:
        with self.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {name}")
            column_defns = ", ".join([
                f"{name} {desc}" for name, desc in columns.items()
            ])
            cur.execute(f"CREATE TABLE {name} ({column_defns})")

    @contextmanager
    def bulk_insert(self, table_name: str, columns: List[str], batch_size: int = 10_000):
        with self.cursor() as cur:
            inserter = BulkInserter(self, table_name, columns, batch_size)
            yield inserter
            inserter.commit()

    @contextmanager
    def insert_many(self, table_name: str, columns: List[str], rows: List[Dict[str, Any]]):
        with self.bulk_insert(table_name, columns) as ins:
            for row in rows:
                ins.add(row)


class BulkInserter:
    def __init__(self, db, table_name: str, columns: List[str], batch_size: int):
        self.db = db
        self.table_name = table_name
        self.columns = columns
        self.rows: List[Any] = []
        self.batch_size = batch_size

    def add(self, row) -> None:
        self.rows.append(row)
        if len(self.rows) >= self.batch_size:
            self.commit()

    def commit(self) -> None:
        numrows = len(self.rows)
        if numrows:
            sql_columns = ", ".join(self.columns)
            sql_column_dict_keys = ", ".join(
                f":{column}" for column in self.columns
            )
            sql = f"INSERT INTO {self.table_name}({sql_columns}) VALUES ({sql_column_dict_keys})"
            with self.db.cursor() as cur:
                print(f"Inserting {numrows} row{'s' if numrows > 1 else ''}.")
                cur.executemany(sql, self.rows)
            self.rows[:] = []


db = Database(DB_PATH)
