"""Tests for the Drills router — list drills and submit attempts."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_drills_requires_auth(client: AsyncClient):
    """GET /drills without auth should return 401."""
    res = await client.get("/api/v1/drills")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_list_drills(client: AsyncClient, auth_headers: dict):
    """GET /drills with auth should return a list."""
    res = await client.get("/api/v1/drills", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_drills_filter_category(client: AsyncClient, auth_headers: dict):
    """GET /drills?category=tactic should filter results."""
    res = await client.get("/api/v1/drills?category=tactic", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    for drill in data:
        assert drill["category"] == "tactic"


@pytest.mark.asyncio
async def test_list_drills_filter_difficulty(client: AsyncClient, auth_headers: dict):
    """GET /drills?difficulty=3 should filter by difficulty."""
    res = await client.get("/api/v1/drills?difficulty=3", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    for drill in data:
        assert drill["difficulty"] == 3


@pytest.mark.asyncio
async def test_attempt_drill_not_found(client: AsyncClient, auth_headers: dict):
    """POST /drills/{bad_id}/attempt should return 404."""
    res = await client.post(
        "/api/v1/drills/00000000-0000-0000-0000-000000000000/attempt",
        headers=auth_headers,
        json={"player_move": "e4", "time_taken_ms": 5000},
    )
    assert res.status_code == 404
