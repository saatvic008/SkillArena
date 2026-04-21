import httpx
from app.config import get_settings

settings = get_settings()

LICHESS_API_BASE = "https://lichess.org/api"


async def fetch_lichess_games(username: str, max_games: int = 20) -> str:
    """Fetch games from Lichess API in PGN format."""
    url = f"{LICHESS_API_BASE}/games/user/{username}"
    params = {
        "max": max_games,
        "opening": "true",
        "evals": "true",
        "clocks": "true",
    }
    headers = {
        "Accept": "application/x-chess-pgn",
    }
    if settings.LICHESS_API_TOKEN:
        headers["Authorization"] = f"Bearer {settings.LICHESS_API_TOKEN}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.text
