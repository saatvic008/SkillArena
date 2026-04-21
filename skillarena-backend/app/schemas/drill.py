import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class DrillResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    difficulty: int
    category: str
    fen_position: str
    correct_move: str
    explanation: str | None = None

    model_config = {"from_attributes": True}


class DrillAttemptCreate(BaseModel):
    player_move: str = Field(..., min_length=2, max_length=10)
    time_taken_ms: int | None = Field(default=None, ge=0)


class DrillAttemptResponse(BaseModel):
    id: uuid.UUID
    drill_id: uuid.UUID
    player_move: str
    is_correct: bool
    time_taken_ms: int | None = None
    attempted_at: datetime
    correct_move: str | None = None
    explanation: str | None = None

    model_config = {"from_attributes": True}
