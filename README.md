# WebCrawler

A Python web crawler that fetches pages, extracts titles and outbound links, stores crawl data in SQLite, tracks dead links, and records page-to-page link relationships.

## What It Does

- Crawls web pages starting from a seed URL
- Extracts page titles
- Collects outbound links
- Stores crawl metadata in SQLite
- Flags dead links using HTTP status codes
- Records graph edges between source and target URLs

## Architecture

- Python
- requests
- BeautifulSoup4
- SQLite
- Java Spring Boot API

The crawler fills `crawler.db`, and the Java API reads from that database to expose crawler data to a frontend or other clients.

## Current Status

Implemented:
- fetch
- parse
- multi-page crawl queue
- SQLite storage
- title search
- dead link tracking
- edge storage for link graph data

Planned:
- graph analysis/query features
- API layer
- better output formatting
- utility helpers and cleanup
