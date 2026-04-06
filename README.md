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
- edge storage for graph data
- Java API for pages and edges

Planned:
- graph analysis/query features
- better output formatting
- project cleanup and utility helpers

## Java API

The Spring Boot API lives in `api/WeirdWebApi-java`.

Available endpoints:
- `GET /health`
- `GET /pages`
- `GET /pages?title=<text>`
- `GET /pages?isDead=0`
- `GET /pages?isDead=1`
- `GET /pages?title=<text>&isDead=1`
- `GET /edges?sourceUrl=<url>`

Example requests:

```text
GET /pages
GET /pages?title=python
GET /pages?isDead=1
GET /edges?sourceUrl=https://example.com
```

## Running The API

From `api/WeirdWebApi-java`:

```bash
./gradlew bootRun
```

By default the API reads the SQLite database from `../../crawler.db`.
You can override that with the `CRAWLER_DB_PATH` environment variable if your database lives somewhere else.
