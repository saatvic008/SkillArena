from fastapi import APIRouter, Request, Query
from app.utils.rate_limiter import limiter
from app.schemas.leaderboard import LeaderboardResponse, LeaderboardEntry
from app.services.cache import get_leaderboard

router = APIRouter()


@router.get("", response_model=LeaderboardResponse)
@limiter.limit("200/minute")
async def get_leaderboard_route(
    request: Request,
    top: int = Query(default=50, ge=1, le=200, description="Number of top players"),
) -> LeaderboardResponse:
    entries = await get_leaderboard(top)
    return LeaderboardResponse(entries=entries, total=len(entries))
