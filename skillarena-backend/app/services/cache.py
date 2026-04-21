import json
from typing import Any

from app.redis_client import get_redis
from app.schemas.leaderboard import LeaderboardEntry

LEADERBOARD_KEY = "leaderboard:global"


async def get_cached(key: str) -> str | None:
    r = get_redis()
    try:
        value = await r.get(key)
        return value
    finally:
        await r.aclose()


async def set_cached(key: str, value: str, ttl: int = 3600) -> None:
    r = get_redis()
    try:
        await r.set(key, value, ex=ttl)
    finally:
        await r.aclose()


async def delete_cached(key: str) -> None:
    r = get_redis()
    try:
        await r.delete(key)
    finally:
        await r.aclose()


async def update_leaderboard(username: str, elo_rating: int) -> None:
    """Add or update a player in the global leaderboard sorted set."""
    r = get_redis()
    try:
        await r.zadd(LEADERBOARD_KEY, {username: elo_rating})
    finally:
        await r.aclose()


async def get_leaderboard(top: int = 50) -> list[LeaderboardEntry]:
    """Get top players from leaderboard sorted set (descending by ELO)."""
    r = get_redis()
    try:
        results = await r.zrevrange(LEADERBOARD_KEY, 0, top - 1, withscores=True)
        entries = []
        for rank, (username, score) in enumerate(results, start=1):
            entries.append(
                LeaderboardEntry(
                    rank=rank,
                    username=username,
                    elo_rating=int(score),
                )
            )
        return entries
    finally:
        await r.aclose()


async def set_session(player_id: str, ws_active: bool = True) -> None:
    """Track player WebSocket session in Redis hash."""
    r = get_redis()
    try:
        key = f"session:{player_id}"
        import time
        await r.hset(key, mapping={
            "ws_active": str(ws_active).lower(),
            "last_seen": str(int(time.time())),
        })
        await r.expire(key, 86400)  # 24 hour TTL
    finally:
        await r.aclose()
