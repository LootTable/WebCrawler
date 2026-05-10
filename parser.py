from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlunparse


def normalize_link(href: str | None) -> str | None:
    if not href:
        return None
    if not href.startswith(("http://", "https://")):
        return None
    parsed = urlparse(href)
    parsed_url = parsed._replace(fragment="")
    return urlunparse(parsed_url)


def parse(response: requests.Response) -> dict:
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.title
    links = set()
    title = None

    for anchor_tag in soup.find_all("a"):
        href = anchor_tag.get("href")
        cleaned_link = normalize_link(href)
        if cleaned_link:
            links.add(cleaned_link)

    if title_tag and title_tag.string:
        clean_title = title_tag.string.strip()
        if clean_title:
            title = clean_title

    return {"title": title, "links": list(links)}

