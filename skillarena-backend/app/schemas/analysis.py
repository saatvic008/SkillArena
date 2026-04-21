import uuid
from datetime import date, datetime
from pydantic import BaseModel
from typing import Any


class WeaknessReportResponse(BaseModel):
    id: uuid.UUID
    player_id: uuid.UUID
    report_date: date
    blunder_rate: float | None = None
    avg_accuracy: float | None = None
    weak_openings: list[dict[str, Any]] | None = None
    weak_endgames: list[dict[str, Any]] | None = None
    tactical_patterns: list[dict[str, Any]] | None = None
    generated_at: datetime | None = None
    recommendations: list["RecommendationResponse"] = []

    model_config = {"from_attributes": True}


class RecommendationResponse(BaseModel):
    id: uuid.UUID
    drill_id: uuid.UUID
    priority: int
    reason: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
