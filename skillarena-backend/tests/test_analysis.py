import pytest


@pytest.mark.asyncio
async def test_get_analysis_no_match(client, auth_headers):
    res = await client.get(
        "/api/v1/analysis/00000000-0000-0000-0000-000000000099/report",
        headers=auth_headers,
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_drills_empty(client, auth_headers):
    res = await client.get("/api/v1/drills", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_drill_attempt_not_found(client, auth_headers):
    res = await client.post(
        "/api/v1/drills/00000000-0000-0000-0000-000000000099/attempt",
        headers=auth_headers,
        json={"player_move": "e4", "time_taken_ms": 5000},
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_leaderboard(client):
    res = await client.get("/api/v1/leaderboard")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_health(client):
    res = await client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
