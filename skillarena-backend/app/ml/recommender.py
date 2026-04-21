import uuid
from typing import Any


# Map weakness profiles to preferred drill categories
PROFILE_DRILL_MAP = {
    "Beginner": ["tactic", "opening", "endgame"],
    "Tactical": ["tactic"],
    "Positional": ["opening", "endgame"],
    "Time-pressure": ["tactic", "endgame"],
}

# Difficulty targeting based on weakness severity
def _target_difficulty(score: float) -> list[int]:
    """Map weakness score (0-100) to appropriate drill difficulties."""
    if score >= 70:
        return [1, 2]      # Severe weakness → easier drills
    elif score >= 40:
        return [2, 3, 4]   # Moderate → mid-range
    else:
        return [3, 4, 5]   # Mild → harder to push growth


def recommend_drills(
    weakness_scores: dict[str, Any],
    available_drills: list[Any],
) -> list[dict[str, Any]]:
    """Rule-based drill recommender.
    
    Maps weakness profile → drill categories, ranks by
    (player weakness score × drill difficulty match), returns top 5.
    """
    profile = weakness_scores.get("profile", "Beginner")
    scores = weakness_scores.get("scores", {})
    
    preferred_categories = PROFILE_DRILL_MAP.get(profile, ["tactic"])
    
    # Compute composite weakness score to determine difficulty targeting
    avg_weakness = sum(scores.values()) / max(len(scores), 1)
    target_difficulties = _target_difficulty(avg_weakness)

    scored_drills: list[tuple[float, Any]] = []
    
    for drill in available_drills:
        if drill.category not in preferred_categories:
            continue
        
        # Score this drill based on category-weakness alignment
        category_score = 0.0
        if drill.category == "tactic":
            category_score = scores.get("tactical", 50)
        elif drill.category == "opening":
            category_score = scores.get("opening", 50)
        elif drill.category == "endgame":
            category_score = scores.get("endgame", 50)

        # Boost score if difficulty matches target range
        difficulty_bonus = 1.5 if drill.difficulty in target_difficulties else 0.5
        
        final_score = category_score * difficulty_bonus
        scored_drills.append((final_score, drill))

    # Sort by score descending, take top 5
    scored_drills.sort(key=lambda x: x[0], reverse=True)
    top_5 = scored_drills[:5]

    recommendations = []
    for priority, (score, drill) in enumerate(top_5, start=1):
        reason = _generate_reason(profile, drill.category, score)
        recommendations.append({
            "drill_id": drill.id,
            "priority": priority,
            "reason": reason,
        })

    return recommendations


def _generate_reason(profile: str, category: str, score: float) -> str:
    """Generate a human-readable reason for the recommendation."""
    reasons = {
        ("Beginner", "tactic"): "Foundation building: practice basic tactical patterns to reduce blunders",
        ("Beginner", "opening"): "Learn key opening principles to avoid early disadvantages",
        ("Beginner", "endgame"): "Improve endgame technique for converting winning positions",
        ("Tactical", "tactic"): "Sharpen tactical vision to spot combinations and avoid oversights",
        ("Positional", "opening"): "Strengthen opening repertoire for better middlegame positions",
        ("Positional", "endgame"): "Practice endgame patterns to improve positional conversions",
        ("Time-pressure", "tactic"): "Train quick pattern recognition to perform under time pressure",
        ("Time-pressure", "endgame"): "Practice endgame speed to avoid time-trouble collapses",
    }
    return reasons.get((profile, category), f"Recommended based on your {profile} profile (weakness score: {score:.0f})")
