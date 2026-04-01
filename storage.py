import sqlite3


def init_db():
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS links(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pages TEXT,
                    url TEXT,
                    title TEXT,
                    status_code INTEGER
                    )""")
        conn.commit()

def savepage(url: str, title: str, status_code: int):
    with sqlite3.connect("crawler.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO links (url, title, status_code) VALUES (?, ?, ?)"
            ,(url, title, status_code)
                    )
        conn.commit()