import httpx

CHESSCOM_API_BASE = "https://api.chess.com/pub"
USER_AGENT = "SkillArena/1.0 (contact: admin@skillarena.dev)"


async def fetch_chesscom_games(username: str, year: int, month: int) -> str:
    """Fetch games from Chess.com API for a specific month, returns PGN text."""
    month_str = str(month).zfill(2)
    url = f"{CHESSCOM_API_BASE}/player/{username}/games/{year}/{month_str}/pgn"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/x-chess-pgn",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        return response.text
