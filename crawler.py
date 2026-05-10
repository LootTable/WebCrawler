from collections import deque
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


def crawl(start_url: str, max_pages: int = 10):
    visited = set()
    queue = deque([start_url])
    queued = {start_url}
    pages_attempted = 0

    while queue:
        url = queue.popleft()
        queued.discard(url)
        if url in visited:
            continue

        results = fetch(url)
        pages_attempted += 1
        if results is None:
            visited.add(url)
            if pages_attempted >= max_pages:
                break
            continue

        is_dead = 1 if results.status_code in (404, 410) else 0

        if is_dead == 1:
            savepage(url, None, results.status_code, is_dead)
        else:
            parsed = parse(results)
            savepage(url, parsed["title"], results.status_code, is_dead)
        
        visited.add(url)
            
        if is_dead != 1:
            for link in parsed["links"]:
                save_edge(url, link)
            
                if link not in visited and link not in queued:
                    queue.append(link)
                    queued.add(link)
        
        if pages_attempted >= max_pages:
            break
        time.sleep(3)
