import uuid
from pydantic import BaseModel


class MoveAnnotationResponse(BaseModel):
    id: uuid.UUID
    annotation_type: str
    engine_best_move: str | None = None
    eval_delta: float | None = None
    annotation_text: str | None = None

    model_config = {"from_attributes": True}


class MoveResponse(BaseModel):
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
    annotations: list[MoveAnnotationResponse] = []

    model_config = {"from_attributes": True}
