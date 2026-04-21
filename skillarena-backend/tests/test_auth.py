import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    res = await client.post("/api/v1/auth/register", json={
        "username": "newplayer",
        "email": "newplayer@example.com",
        "password": "securepass123",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "newplayer"
    assert data["email"] == "newplayer@example.com"
    assert data["elo_rating"] == 1200
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(client):
    await client.post("/api/v1/auth/register", json={
        "username": "dupeuser",
        "email": "dupe@example.com",
        "password": "securepass123",
    })
    res = await client.post("/api/v1/auth/register", json={
        "username": "dupeuser",
        "email": "dupe2@example.com",
        "password": "securepass123",
    })
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "securepass123",
    })
    res = await client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "securepass123",
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    res = await client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "wrongpassword",
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post("/api/v1/auth/register", json={
        "username": "refreshuser",
        "email": "refresh@example.com",
        "password": "securepass123",
    })
    login_res = await client.post("/api/v1/auth/login", json={
        "username": "refreshuser",
        "password": "securepass123",
    })
    refresh_token = login_res.json()["refresh_token"]

    res = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token,
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
