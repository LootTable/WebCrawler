from collections import deque
import time

import requests

from parser import parse
from storage import savepage, save_edge, start_crawl_session, complete_crawl_session


headers = {"User-Agent": "Mozilla/5.0"}


def fetch(url: str) -> requests.Response | None:
    # Keep request failures separate from HTTP errors like 404 or 500.
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error reaching {url}: {e}")
        return None


def crawl(start_url: str, max_pages: int = 10, max_depth: int = 2):
    # Fail early when crawl limits do not make sense.
    if max_pages < 1:
        raise ValueError("max_pages must be at least 1")
    if max_depth < 0:
        raise ValueError("max_depth must be at least 0")

    # One crawl session tracks the overall run, while crawler rows track pages.
    session_id = start_crawl_session(start_url, max_pages, max_depth)
    visited = set()

    # Each queue item stores the URL plus its distance from the start page.
    queue = deque([(start_url, 0)])

    # queued prevents the same URL from piling up before it is crawled.
    queued = {start_url}
    pages_attempted = 0
    request_failures = 0

    while queue:
        url, depth = queue.popleft()
        queued.discard(url)
        if url in visited:
            continue

        results = fetch(url)
        pages_attempted += 1
        if results is None:
            # Network failures still count as attempted pages.
            request_failures += 1
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

        # Only pages below max_depth are allowed to create the next crawl layer.
        if is_dead != 1 and depth < max_depth:
            for link in parsed["links"]:
                # Store the relationship before deciding whether to crawl it.
                save_edge(url, link)

                if link not in visited and link not in queued:
                    queue.append((link, depth + 1))
                    queued.add(link)

        if pages_attempted >= max_pages:
            break
        time.sleep(3)

    # Save the final crawl totals after the queue stops or the page limit is hit.
    complete_crawl_session(session_id, pages_attempted, request_failures)
