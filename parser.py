from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse,urlunparse

def normalize_link(href) -> str | None:
    if not href:
        return None
    if not href.startswith("http://") and not href.startswith("https://"):
        return None
    parsed = urlparse(href)
    parsedUrl = parsed._replace(fragment="")
    return urlunparse(parsedUrl)



def parse(response: requests.Response) -> dict:

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.title
    links = set()    
    
    for anchor_tag in soup.find_all('a'):
        href = anchor_tag.get('href')
        cleaned_link = normalize_link(href)
        if cleaned_link:
            links.add(cleaned_link)
    
    if title_tag and title_tag.string:
        clean_title = title_tag.string.strip()
        return {"title": clean_title if clean_title else None, "links": list(links)}
    else:
        return {"title": None, "links": list(links)}
