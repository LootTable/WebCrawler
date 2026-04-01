# WebCrawler

A simple Python web crawler that fetches pages, extracts titles and links, and stores crawl results in SQLite.

## What it does

- Crawls web pages starting from a seed URL
- Extracts page titles
- Collects outbound links
- Stores crawl metadata in SQLite

## Current Stack

- Python
- requests
- BeautifulSoup4
- SQLite

## Current Status

- Implemented: fetch, parse, store, basic crawl queue
- Planned: search, link graph analysis, dead link detection, API layer
