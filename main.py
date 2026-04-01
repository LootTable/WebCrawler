import requests
from bs4 import BeautifulSoup
from storage import init_db, savepage
import time
URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
headers = {"User-Agent": "Mozilla/5.0"}


def fetch(url:str)-> requests.Response | None:
    try:
        response = requests.get(url,headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error reaching {url}: {e}")


def parse(response: requests.Response) -> dict:
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.title
    aLinks = []    
    
    for anchor_tag in soup.find_all('a'):
        href = anchor_tag.get('href')
        if href and href.startswith("http"):
            aLinks.append(href)

    
    if title_tag:
        return {"title": title_tag.string , 'links': aLinks}
    else:
        return{"title": None, "Links": []}

def crawl(start_url: str):
    visited = set()
    queue = [start_url]
    count = 0
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        else:
            results = fetch(url)
            if results is None:
                continue
            parsed = parse(results)
            savepage(url, parsed["title"], results.status_code)
            visited.add(url)
            queue.extend(parsed["links"])
            count += 1
            if count >= 10:
                break
            time.sleep(3)




if __name__ == "__main__":
    init_db()
    crawl(URL)