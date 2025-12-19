from pathlib import Path
import sqlite3
from typing import Self


class Database:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.CREATE_QUERY = """CREATE TABLE IF NOT EXISTS {} (label TEXT, description TEXT, type TEXT, PRIMARY KEY (label));"""
        self.INSERT_QUERY = (
            "INSERT OR IGNORE INTO {} (label, description, type) VALUES (?, ?, ?)"
        )
        self.READ_LABEL_QUERY = "SELECT label FROM {} WHERE type = ?"
        self.READ_DESCRIPTION_QUERY = (
            "SELECT description FROM {} WHERE label =  ? AND type = ?"
        )
        self.TABLES = {"presets": "presets"}
        self.conn = self._connect()

    def _connect(self, timeout: int = 30) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path), timeout=timeout, detect_types=sqlite3.PARSE_DECLTYPES
        )
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA busy_timeout = 30000;")
        return conn

    def _init_schema(self, create_table_query: str) -> None:
        cur = self.conn.cursor()
        cur.execute(create_table_query)
        cur.close()

    def _drop_table(self, table_name: str):
        with self.conn:
            cursor = self.conn.cursor()
            query = f"DROP TABLE {table_name}"
            cursor.execute(query)

    def _insert_data(self, query: str, params: tuple):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)

    # def _update_data(self, query: str, params: tuple):
    #     with self.conn:
    #         cursor = self.conn.cursor()

    def _execute_query(self, query: str, params: tuple, fallback_func: callable = None):
        try:
            with self.conn:

                cursor = self.conn.cursor()
                data = cursor.execute(query, params)
                return data.fetchall()
        except sqlite3.OperationalError:
            if fallback_func is not None:
                fallback_func()
                self._execute_query(query, params)

    def close(self) -> None:
        try:
            self.conn.commit()
        except Exception:
            pass
        self.conn.close()

    # context manager support
    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def create_presets_table(self):
        self._init_schema(self.CREATE_QUERY.format(self.TABLES["presets"]))

    #######################################
    # Action
    #######################################

    def insert_data(self, label: str, description: str, preset_type: str):
        self._execute_query(
            self.INSERT_QUERY.format(self.TABLES["presets"]),
            params=(label, description, preset_type),
            fallback_func=self.create_presets_table,
        )

    def delete_data(self, label: str):
        query = f"DELETE FROM {self.TABLES['presets']} WHERE label = ?"
        params = (label,)
        self._execute_query(query, params, fallback_func=self.create_presets_table)

    def read_labels(self, preset_type: str, get_all: bool = False) -> list:
        if get_all:
            data = self._execute_query(
                f"SELECT label FROM {self.TABLES['presets']}",
                (),
                fallback_func=self.create_presets_table,
            )
        else:
            data = self._execute_query(
                self.READ_LABEL_QUERY.format(self.TABLES["presets"]),
                (preset_type,),
                self.create_presets_table,
            )
        return data

    def read_description(self, label: str, preset_type: str) -> list:
        data = self._execute_query(
            self.READ_DESCRIPTION_QUERY.format(self.TABLES["presets"]),
            (label, preset_type),
            self.create_presets_table,
        )
        return data

    def update_data(self, label: str, new_description: str):
        self._execute_query(
            f"""UPDATE presets SET description = ? WHERE label  = ?""",
            params=(new_description, label),
            fallback_func=self.create_presets_table,
        )


def _get_presets() -> str:
    presets = ["action", "subject", "location"]
    return presets


if __name__ == "__main__":

    db = Database("presets.db")

    # db.insert_subject("Test", "This is a test")
    labels = db.read_labels("subject")
    print(labels)
