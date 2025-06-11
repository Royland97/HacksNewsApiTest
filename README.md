# HacksNewsApiTest
This project is a FastAPI-based web API that scrapes and caches articles from [Hacker News](https://news.ycombinator.com/). It uses asynchronous HTTP requests, fast HTML parsing, and an in-memory cache with TTL to reduce redundant network calls.

Requirements
- Python 3.10+
- Docker

For local deployment install dependencies:
<pre>pip install -r requirements.txt</pre>

Running with Docker
<pre>docker-compose up --build -d</pre>

Stop the service
<pre>docker-compose down</pre>

Api EndPoints:
| Method | Path             | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | `/`              | Get Hacker News page 1   |
| GET    | `/{page_number}` | Get specific page (1+)   |
| GET    | `/cache/status`  | View cache keys and size |
| POST   | `/cache/clear`   | Clear all cached pages   |

Running Tests:

Tests should be written using pytest. If you're using a tests/ folder, run:
<pre>pytest</pre>

With docker:

<pre>docker-compose run test</pre>
 