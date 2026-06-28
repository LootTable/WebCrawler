# WebCrawler

A Python web crawler that fetches pages, extracts titles and outbound links, stores crawl data in PostgreSQL, tracks dead links, and records page-to-page link relationships. A Java Spring Boot API and dashboard read from the same database so crawled results can be searched and inspected in the browser.

## What It Does

- Crawls web pages starting from a seed URL
- Extracts page titles
- Collects outbound links
- Stores crawl metadata in PostgreSQL
- Flags dead links using HTTP status codes
- Records graph edges between source and target URLs
- Tracks crawl sessions, including the start URL, page limit, depth limit, attempted pages, request failures, and completion time

## Architecture

- Python
- requests
- BeautifulSoup4
- PostgreSQL
- Java Spring Boot API

The Python crawler writes to PostgreSQL, and the Java API reads from that same database to expose crawler data to the dashboard or other clients. The SQLite implementation is still kept in `storage_sqlite.py` as a reference, while `storage.py` currently points the application at `storage_postgres.py`.

## Current Status

Implemented:
- fetch
- parse
- multi-page crawl queue
- PostgreSQL storage
- crawl session tracking
- title search
- dead link tracking
- edge storage for link graph data
- Java API for pages and edges
- built-in dashboard served by Spring Boot

Planned:
- graph analysis/query features
- better output formatting
- utility helpers and cleanup

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

## Dashboard

The Spring Boot app also serves a lightweight dashboard at:

```text
GET /
```

The dashboard lets you:
- browse crawled pages
- filter by title and dead/alive status
- select a page and inspect its outbound edges

## Database Setup

Create the local PostgreSQL database before running the crawler or Java API:

```bash
createdb crawler
```

The Python crawler uses this connection by default:

```text
postgresql://nicholasmckendall@localhost:5432/crawler
```

You can override it with:

```bash
export DATABASE_URL="postgresql://your_user@localhost:5432/crawler"
```

Initialize the database tables:

```bash
python -c "from storage import init_db; init_db(); print('tables created')"
```

## Running The Crawler

From the project root:

```bash
python main.py
```

The crawler will ask for:

- the starting URL
- the maximum number of pages to attempt
- the maximum crawl depth
- a search query to run against saved page titles

## Running The API

From `api/WeirdWebApi-java`:

```bash
./gradlew bootRun
```

By default the API reads from:

```text
jdbc:postgresql://localhost:5432/crawler
```

You can override the Java database connection with:

```bash
export SPRING_DATASOURCE_URL="jdbc:postgresql://localhost:5432/crawler"
export SPRING_DATASOURCE_USERNAME="your_user"
```

Once the app is running, open:

```text
http://localhost:8080/
```
