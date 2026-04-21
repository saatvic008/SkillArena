from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    elo_rating: int
    games_played: int | None = None
    win_rate: float | None = None


class LeaderboardResponse(BaseModel):
    entries: list[LeaderboardEntry]
    total: int
