from cachetools import TTLCache

# TTLCache(maxsize, ttl)
html_cache = TTLCache(maxsize=100, ttl=300)  # Max 100 pages, 5 minutes TTL
