import pytest


SAMPLE_PGN = """[Event "Test Game"]
[Site "Test"]
[Date "2025.06.15"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]
[ECO "B20"]
[Opening "Sicilian Defense"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 1-0
"""


@pytest.mark.asyncio
async def test_list_matches_empty(client, auth_headers):
    res = await client.get("/api/v1/matches", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 0
    assert data["matches"] == []


@pytest.mark.asyncio
async def test_upload_pgn(client, auth_headers):
    files = {"file": ("test.pgn", SAMPLE_PGN.encode(), "application/x-chess-pgn")}
    res = await client.post("/api/v1/matches/upload", headers=auth_headers, files=files)
    assert res.status_code == 201
    data = res.json()
    assert data["total"] >= 1
    match = data["matches"][0]
    assert match["source"] == "upload"
    assert match["result"] in ("win", "loss", "draw")


@pytest.mark.asyncio
async def test_upload_invalid_extension(client, auth_headers):
    files = {"file": ("test.txt", b"not a pgn", "text/plain")}
    res = await client.post("/api/v1/matches/upload", headers=auth_headers, files=files)
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_get_match_not_found(client, auth_headers):
    res = await client.get(
        "/api/v1/matches/00000000-0000-0000-0000-000000000099",
        headers=auth_headers,
    )
    assert res.status_code == 404
