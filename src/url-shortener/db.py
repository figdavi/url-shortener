import sqlite3
from pydantic import HttpUrl

DB_NAME = "urls.db"

def create_table():
    """Creates the 'shortened_urls' table"""
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS shortened_urls(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            original_url TEXT NOT NULL,
                            short_code TEXT NOT NULL
                        )
                        """)


def insert_url(url: HttpUrl, short_code: str):
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        while True:
            query_result = cursor.execute(
                """
                SELECT original_url 
                FROM shortened_urls 
                WHERE short_code = ?
                """,
                (short_code,),
            )

            row = query_result.fetchone()

            # If no url registered under generated short code, insert
            if row is None:
                cursor.execute(
                    """
                    INSERT INTO shortened_urls (original_url, short_code)
                            VALUES (?, ?)
                            """,
                    (
                        str(url),
                        short_code,
                    ),
                )
                break
