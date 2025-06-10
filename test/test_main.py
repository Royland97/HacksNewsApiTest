import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_default_page_returns_30():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 30
    assert all("title" in item for item in response.json())

@pytest.mark.asyncio
async def test_multiple_pages():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/2")
    assert response.status_code == 200
    assert len(response.json()) == 60

@pytest.mark.asyncio
async def test_invalid_page():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/0")
    assert response.status_code == 422
