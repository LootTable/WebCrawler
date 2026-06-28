import sqlite3


def init_db():
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        # crawler stores one row per URL that has been attempted.
        cursor.execute("""CREATE TABLE IF NOT EXISTS crawler(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    status_code INTEGER,
                    is_dead INTEGER DEFAULT 0
                    )""")

        # edges stores the page-to-page relationships discovered by the crawler.
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS edges(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT,
                    target_url TEXT,
                    UNIQUE(source_url, target_url)
                    )""")

        # crawl_sessions stores one summary row for each crawler run.
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS crawl_sessions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        start_url TEXT NOT NULL,
                        max_pages INTEGER NOT NULL CHECK(max_pages > 0),
                        max_depth INTEGER NOT NULL CHECK(max_depth >= 0),
                        pages_attempted INTEGER NOT NULL DEFAULT 0,
                        request_failures INTEGER NOT NULL DEFAULT 0,
                        started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        completed_at TEXT
                    )
        """)
        conn.commit()


def start_crawl_session(start_url: str, max_pages: int, max_depth: int) -> int:
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        # Store the run settings first, then update totals when the crawl ends.
        cursor.execute(
            """
            INSERT INTO crawl_sessions(start_url, max_pages, max_depth)
            VALUES (?, ?, ?)
            """,
            (start_url, max_pages, max_depth)
        )
        session_id = cursor.lastrowid
        conn.commit()
        return session_id


def complete_crawl_session(
    session_id: int,
    pages_attempted: int,
    request_failures: int,
):
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        # Update the same session row that was created when the crawl started.
        cursor.execute(
            """
            UPDATE crawl_sessions
            SET pages_attempted = ?, request_failures = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (pages_attempted, request_failures, session_id)
        )
        conn.commit()


def savepage(url: str, title: str | None, status_code: int, is_dead: int):
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        # Re-crawling a URL should refresh the row instead of creating a duplicate.
        cursor.execute(
            """
            INSERT INTO crawler (url, title, status_code, is_dead)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                status_code = excluded.status_code,
                is_dead = excluded.is_dead
            """,
            (url, title, status_code, is_dead)
        )
        conn.commit()


def save_edge(source_url: str, target_url: str):
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        # Duplicate edges can happen naturally when pages link to the same URL.
        cursor.execute(
            "INSERT OR IGNORE INTO edges (source_url, target_url) VALUES (?, ?)",
            (source_url, target_url),
        )
        conn.commit()


def get_dead_links() -> list:
    with sqlite3.connect("crawler.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crawler WHERE is_dead = 1")
        results = cursor.fetchall()
        return [dict(row) for row in results]


def search_pages(query: str) -> list:
    with sqlite3.connect("crawler.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crawler WHERE title LIKE ?", (f"%{query}%",))
        results = cursor.fetchall()
        return [dict(row) for row in results]
