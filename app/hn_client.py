import httpx
from selectolax.parser import HTMLParser
from asyncio import gather
from app.models import News
from app.cache import html_cache

BASE_URL = "https://news.ycombinator.com/news?p={}"

async def fetch_page_html(page: int) -> str:
    if page in html_cache:
        return html_cache[page]

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL.format(page))
        response.raise_for_status()
        html_cache[page] = response.text
        return response.text

def parse_page(html: str) -> list[News]:
    tree = HTMLParser(html)
    articles = []

    rows = tree.css("tr.athing") # Main post rows
    subtexts = tree.css("td.subtext") # Subtext rows that contain points, author, and comments

    for row, sub in zip(rows, subtexts):
        # Find the story link and title
        title_node = row.css_first("a.storylink") or row.css_first("span.titleline a")
        if not title_node:
            continue

        title = title_node.text(strip=True)
        url = title_node.attributes.get("href", "")
        if url.startswith("item?"):
            url = f"https://news.ycombinator.com/{url}" # Convert relative links to absolute

        #Extract points if available
        points_node = sub.css_first("span.score")
        points = int(points_node.text().split()[0]) if points_node else 0

        # Extract author if available
        author_node = sub.css_first("a.hnuser")
        sent_by = author_node.text(strip=True) if author_node else "unknown"

        # Extract relative publish time
        time_node = sub.css_first("span.age")
        published = time_node.text(strip=True) if time_node else "unknown"

        # Extract number of comments
        comments = 0
        comment_links = sub.css("a")
        if comment_links:
            last_link = comment_links[-1]
            text = last_link.text()
            if "comment" in text:
                try:
                    comments = int(text.split()[0])
                except ValueError:
                    comments = 0

        news_item = News(
            title=title,
            url=url,
            points=points,
            author=sent_by,
            published=published,
            comments=comments
        )
        articles.append(news_item)

    return articles

async def fetch_page(pages: int = 1) -> list[News]:
    # Determine missing pages that aren't already in cache
    missing_pages = [i for i in range(1, pages + 1) if i not in html_cache]

    # Create async fetch tasks for all requested pages
    html_tasks = [fetch_page_html(i) for i in missing_pages]
    await gather(*html_tasks)

    all_articles = []
    # Parse each page and combine all articles into a single list
    for i in range(1, pages + 1):
        html = html_cache[i]
        all_articles.extend(parse_page(html))

    return all_articles
