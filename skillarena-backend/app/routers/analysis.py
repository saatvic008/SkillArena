import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.player import Player
from app.models.match import Match
from app.models.weakness_report import WeaknessReport
from app.schemas.analysis import WeaknessReportResponse
from app.utils.auth_utils import get_current_player
from app.utils.rate_limiter import limiter
from app.services.cache import get_cached, set_cached
from app.services.report_service import generate_weakness_report

router = APIRouter()


@router.get("/{match_id}/report", response_model=WeaknessReportResponse)
@limiter.limit("200/minute")
async def get_analysis_report(
    request: Request,
    match_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> WeaknessReportResponse:
    # Check cache first
    cache_key = f"analysis:{match_id}"
    cached = await get_cached(cache_key)
    if cached:
        return WeaknessReportResponse.model_validate_json(cached)

    # Verify match belongs to player
    match_result = await db.execute(
        select(Match).where(Match.id == match_id, Match.player_id == player.id)
    )
    match = match_result.scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Check for existing report
    report_result = await db.execute(
        select(WeaknessReport)
        .where(WeaknessReport.player_id == player.id)
        .order_by(WeaknessReport.report_date.desc())
        .limit(1)
    )
    report = report_result.scalar_one_or_none()

    if report and report.generated_at is not None:
        response = WeaknessReportResponse.model_validate(report)
        await set_cached(cache_key, response.model_dump_json(), ttl=3600)
        return response

    # No completed report — generate one in background
    if report and report.generated_at is None:
        background_tasks.add_task(generate_weakness_report, player.id, report.id)
        raise HTTPException(
            status_code=202,
            detail="Report is being generated. Please retry in a few seconds.",
        )

    # Create a new pending report and trigger generation
    new_report = WeaknessReport(player_id=player.id)
    db.add(new_report)
    await db.flush()
    await db.refresh(new_report)
    background_tasks.add_task(generate_weakness_report, player.id, new_report.id)
    raise HTTPException(
        status_code=202,
        detail="Report generation started. Please retry in a few seconds.",
    )
