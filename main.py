
from storage import init_db, search_pages, get_dead_links
from crawler import crawl

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"

if __name__ == "__main__":
    init_db()
    crawl(URL)
    print(search_pages("Python"))
    print(get_dead_links())