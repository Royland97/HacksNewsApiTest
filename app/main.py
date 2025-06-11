from fastapi import FastAPI, Path, HTTPException
from app.hn_client import fetch_page
from typing import List
from app.models import News
from app.cache import html_cache
app = FastAPI()

@app.get("/", response_model=List[News])
async def root():
    return await fetch_page(1)

@app.get("/{page_number}", response_model=List[News])
async def get_news(page_number: int = Path(..., gt=0)):
    if page_number < 1:
        raise HTTPException(status_code=400, detail="Page number must be >= 1")
    return await fetch_page(page_number)

@app.post("/cache/clear")
async def clear_cache():
    html_cache.clear()
    return {"detail": "Cache cleared"}

@app.get("/cache/status")
async def cache_status():
    return {
        "cached_pages": list(html_cache.keys()),
        "cache_size": len(html_cache),
        "max_cache_size": html_cache.maxsize
    }
