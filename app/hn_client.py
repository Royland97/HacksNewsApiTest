import httpx
from selectolax.parser import HTMLParser

BASE_URL = "https://news.ycombinator.com/news?p={}"

async def fetch_page_html(page: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL.format(page))
        response.raise_for_status()
        return response.text

def parse_page(html: str) -> list:
    tree = HTMLParser(html)
    articles = []

    rows = tree.css("tr.athing")
    subtexts = tree.css("td.subtext")

    for row, sub in zip(rows, subtexts):
        title_node = row.css_first("a.storylink") or row.css_first("span.titleline a")
        if not title_node:
            continue

        title = title_node.text(strip=True)
        url = title_node.attributes.get("href", "")
        if url.startswith("item?"):
            url = f"https://news.ycombinator.com/{url}"

        points_node = sub.css_first("span.score")
        points = int(points_node.text().split()[0]) if points_node else 0

        author_node = sub.css_first("a.hnuser")
        sent_by = author_node.text(strip=True) if author_node else "unknown"

        time_node = sub.css_first("span.age")
        published = time_node.text(strip=True) if time_node else "unknown"

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

        articles.append({
            "title": title,
            "url": url,
            "points": points,
            "author": sent_by,
            "published": published,
            "comments": comments
        })

    return articles

async def fetch_page(pages: int = 1) -> list:
    from asyncio import gather
    html_tasks = [fetch_page_html(i) for i in range(1, pages + 1)]
    html_pages = await gather(*html_tasks)
    all_articles = []
    for html in html_pages:
        all_articles.extend(parse_page(html))
    return all_articles
