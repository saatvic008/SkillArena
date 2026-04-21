import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.player import Player
from app.models.drill import Drill
from app.models.drill_attempt import DrillAttempt
from app.schemas.drill import DrillResponse, DrillAttemptCreate, DrillAttemptResponse
from app.utils.auth_utils import get_current_player
from app.utils.rate_limiter import limiter

router = APIRouter()


@router.get("", response_model=list[DrillResponse])
@limiter.limit("200/minute")
async def list_drills(
    request: Request,
    category: str | None = Query(default=None, description="Filter by category: tactic, endgame, opening"),
    difficulty: int | None = Query(default=None, ge=1, le=5, description="Filter by difficulty 1-5"),
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _player: Player = Depends(get_current_player),
) -> list[DrillResponse]:
    query = select(Drill)
    if category:
        query = query.where(Drill.category == category)
    if difficulty:
        query = query.where(Drill.difficulty == difficulty)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    drills = result.scalars().all()
    return [DrillResponse.model_validate(d) for d in drills]


@router.post("/{drill_id}/attempt", response_model=DrillAttemptResponse)
@limiter.limit("200/minute")
async def attempt_drill(
    request: Request,
    drill_id: uuid.UUID,
    body: DrillAttemptCreate,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> DrillAttemptResponse:
    result = await db.execute(select(Drill).where(Drill.id == drill_id))
    drill = result.scalar_one_or_none()
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")

    is_correct = body.player_move.strip().lower() == drill.correct_move.strip().lower()

    attempt = DrillAttempt(
        player_id=player.id,
        drill_id=drill.id,
        player_move=body.player_move,
        is_correct=is_correct,
        time_taken_ms=body.time_taken_ms,
    )
    db.add(attempt)
    await db.flush()
    await db.refresh(attempt)

    return DrillAttemptResponse(
        id=attempt.id,
        drill_id=attempt.drill_id,
        player_move=attempt.player_move,
        is_correct=attempt.is_correct,
        time_taken_ms=attempt.time_taken_ms,
        attempted_at=attempt.attempted_at,
        correct_move=drill.correct_move if not is_correct else None,
        explanation=drill.explanation if not is_correct else None,
    )
