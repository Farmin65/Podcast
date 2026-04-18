import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from ..config import config

class Database:
    def __init__(self):
        self.config = config

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(
            dbname=self.config.DB_NAME,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            host=self.config.DB_HOST,
            port=self.config.DB_PORT,
            client_encoding='WIN1251'
        )
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def get_cursor(self, commit=False):
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(query, params or ())
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            return cursor.rowcount

db = Database()