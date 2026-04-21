import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.move import Move
from app.models.weakness_report import WeaknessReport
from app.models.drill import Drill
from app.models.recommendation import Recommendation
from app.ml.feature_extractor import extract_features
from app.ml.weakness_scorer import score_weaknesses
from app.ml.recommender import recommend_drills


async def generate_weakness_report(player_id: uuid.UUID, report_id: uuid.UUID) -> None:
    """Background task: run ML pipeline and update the weakness report."""
    async with AsyncSessionLocal() as db:
        # Fetch all moves for this player via their matches
        from app.models.match import Match
        match_result = await db.execute(
            select(Match.id).where(Match.player_id == player_id)
        )
        match_ids = [row[0] for row in match_result.fetchall()]

        if not match_ids:
            return

        moves_result = await db.execute(
            select(Move).where(Move.match_id.in_(match_ids)).order_by(Move.move_number)
        )
        moves = moves_result.scalars().all()

        if not moves:
            return

        # ML Pipeline
        features_df = extract_features(moves)
        weakness_scores = score_weaknesses(features_df)
        
        # Fetch available drills
        drills_result = await db.execute(select(Drill))
        drills = drills_result.scalars().all()
        
        recommended = recommend_drills(weakness_scores, drills)

        # Update the report
        report_result = await db.execute(
            select(WeaknessReport).where(WeaknessReport.id == report_id)
        )
        report = report_result.scalar_one_or_none()
        if not report:
            return

        report.blunder_rate = weakness_scores.get("blunder_rate", 0.0)
        report.avg_accuracy = weakness_scores.get("avg_accuracy", 0.0)
        report.weak_openings = weakness_scores.get("weak_openings", [])
        report.weak_endgames = weakness_scores.get("weak_endgames", [])
        report.tactical_patterns = weakness_scores.get("tactical_patterns", [])
        report.generated_at = datetime.now(timezone.utc)

        # Create recommendations
        for rec in recommended:
            recommendation = Recommendation(
                player_id=player_id,
                report_id=report_id,
                drill_id=rec["drill_id"],
                priority=rec["priority"],
                reason=rec["reason"],
            )
            db.add(recommendation)

        await db.commit()
