import sqlite3
from pydantic import HttpUrl
import secrets
from datetime import datetime

DB_NAME = "urls.db"

def generate_short_code() -> str:
    """Generates a random URL-safe 4 byte string

    Returns:
        str: The random string
    """
    return secrets.token_urlsafe(4)

def get_current_time_iso():
    return datetime.now().isoformat('T', 'seconds')

def create_table():
    """Creates the 'shortened_urls' table"""
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS shortened_urls(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT NOT NULL,
                            short_code TEXT NOT NULL,
                            created_at TEXT NOT NULL,
                            updated_at TEXT NOT NULL
                        )
                        """)


def insert_url(url: HttpUrl) -> str:
    insert_sql = """
    INSERT INTO shortened_urls (url, short_code, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """
    
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        while True:
            short_code = generate_short_code()
            query_result = cursor.execute(
                """
                SELECT 1 
                FROM shortened_urls 
                WHERE short_code = ?
                """,
                (short_code,),
            )

            row = query_result.fetchone()

            # If no url registered under generated short code, insert
            if row is None:
                cur_time = get_current_time_iso()
                cursor.execute(insert_sql,
                               (str(url), short_code, cur_time, cur_time),
                               )
                return short_code
