from fastapi import FastAPI, Path, HTTPException
from app.hn_client import fetch_page
from typing import List
from app.models import News
app = FastAPI()

@app.get("/", response_model=List[News])
async def root():
    return await fetch_page(1)

@app.get("/{page_number}", response_model=List[News])
async def get_news(page_number: int = Path(..., gt=0)):
    if page_number < 1:
        raise HTTPException(status_code=400, detail="Page number must be >= 1")
    return await fetch_page(page_number)
