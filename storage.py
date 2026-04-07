import sqlite3


def init_db():
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS crawler(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    status_code INTEGER,
                    is_dead INTEGER DEFAULT 0
                       )""")
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS edges(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT,
                    target_url TEXT,
                    UNIQUE(source_url, target_url)
                       )""")
        conn.commit()


def savepage(url: str, title: str, status_code: int, is_dead: int):
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
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
        cursor.execute(
            "INSERT OR IGNORE INTO edges(source_url, target_url) VALUES(?,?)",
            (source_url, target_url))
        conn.commit()


def get_dead_links() -> list:
    with sqlite3.connect("crawler.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM crawler WHERE is_dead = 1 ")
        results = cursor.fetchall()
        return [dict(row) for row in results]




def search_pages(query: str) -> list:
    with sqlite3.connect("crawler.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
        "SELECT * FROM crawler WHERE title LIKE ? ",(f"%{query}%",)
        )
        results = cursor.fetchall()
        return [dict(row) for row in results]

