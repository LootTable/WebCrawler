import os

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nicholasmckendall@localhost:5432/crawler",
)

def init_db():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            # crawler stores one row per URL that has been attempted.
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS crawler(
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    title TEXT,
                    status_code INTEGER NOT NULL,
                    is_dead INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            
            # edges stores the page-to-page relationships discovered by the crawler.
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS edges(
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    source_url TEXT NOT NULL,
                    target_url TEXT NOT NULL,
                    UNIQUE(source_url, target_url)
                )
                """
            )
            
            # crawl_sessions stores one summary row for each crawler run.
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS crawl_sessions(
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    start_url TEXT NOT NULL,
                    max_pages INTEGER NOT NULL CHECK(max_pages > 0),
                    max_depth INTEGER NOT NULL CHECK(max_depth >= 0),
                    pages_attempted INTEGER NOT NULL DEFAULT 0,
                    request_failures INTEGER NOT NULL DEFAULT 0,
                    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                )
                """
            )


def start_crawl_session(start_url: str, max_pages: int, max_depth: int) -> int:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO crawl_sessions(start_url, max_pages, max_depth)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (start_url, max_pages, max_depth)
                )
            session_id = cursor.fetchone()[0]
            return session_id
        
def complete_crawl_session(
    session_id: int,
    pages_attempted: int,
    request_failures: int,
): 
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE crawl_sessions
                SET pages_attempted = %s, request_failures = %s, completed_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (pages_attempted, request_failures, session_id)
                )
            
def savepage(url: str, title: str | None, status_code: int, is_dead: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO crawler (url, title, status_code, is_dead)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(url) DO UPDATE SET
                    title = excluded.title,
                    status_code = excluded.status_code,
                    is_dead = excluded.is_dead
                """,
                (url, title, status_code, is_dead)
            )

def save_edge(source_url: str, target_url: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO edges (source_url, target_url)
                VALUES (%s, %s)
                ON CONFLICT (source_url, target_url) DO NOTHING
                """,
                (source_url, target_url),
            )

def get_dead_links() -> list:
    with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM crawler WHERE is_dead = 1")
            results = cursor.fetchall()
            return [dict(row) for row in results]
        
def search_pages(query: str) -> list:
    with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM crawler WHERE title ILIKE %s", (f"%{query}%",))
            results = cursor.fetchall()
            return [dict(row) for row in results]
