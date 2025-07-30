import sqlite3
import secrets
from datetime import datetime, timezone
from .models import URLModel

DB_NAME = "urls.db"

def generate_short_code() -> str:
    """Generates a random URL-safe 4 byte string

    Returns:
        str: The random string
    """
    return secrets.token_urlsafe(4)

def get_current_time() -> str:
    """Return current datetime in the following format: YYYY-MM-dd'T'HH:MM:SS'Z'\n
    Example: "2021-09-01T12:00:00Z"

    Returns:
        str: Current datetime in specified format
    """     
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def create_table():
    """Creates the "shortened_urls" table"""
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


def insert_url(url: URLModel) -> str:
    insert_sql = """
    INSERT INTO shortened_urls (url, short_code, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """
    
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        while True:
            short_code = generate_short_code()
            select_sql = """
            SELECT 1 
            FROM shortened_urls 
            WHERE short_code = ?
            """
            
            query_result = cursor.execute(
                select_sql,
                (short_code,)
            )

            row = query_result.fetchone()

            # If no url registered under generated short code, insert
            if row is None:
                cur_time = get_current_time()
                cursor.execute(insert_sql,
                               (str(url), short_code, cur_time, cur_time)
                               )
                return short_code

def get_url(short_code: str) -> URLModel:
    select_sql = """
    SELECT url FROM shortened_urls
        WHERE short_code = ?
    """
    
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute(select_sql, (short_code,))

        result = cursor.fetchone()
        
        if result:
            url = URLModel(url=result[0])
            return url
        else:
            raise ValueError(f"URL associated with {short_code} does not exist.")
    