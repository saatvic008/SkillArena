import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any


class MatchResponse(BaseModel):
    id: uuid.UUID
    source: str
    opponent_username: str | None = None
    result: str
    opening_name: str | None = None
    opening_eco: str | None = None
    time_control: str | None = None
    played_at: datetime
    metadata: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class MatchListResponse(BaseModel):
    matches: list[MatchResponse]
    total: int


class MoveInMatch(BaseModel):
    id: uuid.UUID
    move_number: int
    color: str
    san: str
    uci: str
    fen_before: str
    fen_after: str
    eval_score: float | None = None
    move_time_ms: int | None = None
    is_blunder: bool
    is_mistake: bool

    model_config = {"from_attributes": True}


class MatchDetailResponse(BaseModel):
    id: uuid.UUID
    source: str
    opponent_username: str | None = None
    result: str
    opening_name: str | None = None
    opening_eco: str | None = None
    time_control: str | None = None
    played_at: datetime
    pgn_raw: str | None = None
    metadata: dict[str, Any] | None = None
    moves: list[MoveInMatch] = []

    model_config = {"from_attributes": True}


class FetchLichessRequest(BaseModel):
    lichess_username: str = Field(..., min_length=1, max_length=50)
    max_games: int = Field(default=20, ge=1, le=100)


class FetchChesscomRequest(BaseModel):
    chesscom_username: str = Field(..., min_length=1, max_length=50)
    year: int = Field(default=2025, ge=2000, le=2030)
    month: int = Field(default=1, ge=1, le=12)
