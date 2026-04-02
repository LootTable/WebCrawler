import time
import requests
from parser import parse
from storage import savepage, save_edge

headers = {"User-Agent": "Mozilla/5.0"}


def fetch(url: str) -> requests.Response | None:
    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error reaching {url}: {e}")
        return None


def crawl(start_url: str):
    visited = set()
    queue = [start_url]
    count = 0

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue

        results = fetch(url)
        if results is None:
            continue

        is_dead = 1 if results.status_code in (404, 410) else 0

        if is_dead == 1:
            savepage(url, None, results.status_code, is_dead)
            visited.add(url)
            count += 1
            if count >= 10:
                break
            time.sleep(3)
            continue

        parsed = parse(results)
        savepage(url, parsed["title"], results.status_code, is_dead)
        for link in parsed["links"]:
            save_edge(url,link)
        visited.add(url)
        queue.extend(parsed["links"])
        count += 1
        if count >= 10:
            break
        time.sleep(3)
