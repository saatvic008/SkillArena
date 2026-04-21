import pandas as pd
import numpy as np
from typing import Any


def extract_features(moves: list[Any]) -> pd.DataFrame:
    """Extract player performance features from a list of Move ORM objects.
    
    Returns a single-row DataFrame with computed features.
    """
    total_moves = len(moves)
    if total_moves == 0:
        return pd.DataFrame([_empty_features()])

    blunders = sum(1 for m in moves if m.is_blunder)
    mistakes = sum(1 for m in moves if m.is_mistake)
    
    eval_scores = [m.eval_score for m in moves if m.eval_score is not None]
    move_times = [m.move_time_ms for m in moves if m.move_time_ms is not None]

    # Compute eval drops between consecutive moves
    eval_drops = []
    for i in range(1, len(eval_scores)):
        drop = abs(eval_scores[i] - eval_scores[i - 1])
        eval_drops.append(drop)

    # Separate opening (first 10 moves), middlegame, and endgame phases
    opening_moves = [m for m in moves if m.move_number <= 10]
    endgame_moves = [m for m in moves if m.move_number > 30]
    
    opening_blunders = sum(1 for m in opening_moves if m.is_blunder)
    endgame_blunders = sum(1 for m in endgame_moves if m.is_blunder)
    
    # Time pressure: moves made in under 10 seconds
    time_pressure_moves = [m for m in moves if m.move_time_ms is not None and m.move_time_ms < 10000]
    time_pressure_blunders = sum(1 for m in time_pressure_moves if m.is_blunder)

    features = {
        "blunder_rate": blunders / total_moves if total_moves > 0 else 0.0,
        "mistake_rate": mistakes / total_moves if total_moves > 0 else 0.0,
        "inaccuracy_rate": (blunders + mistakes) / total_moves if total_moves > 0 else 0.0,
        "avg_eval_drop": float(np.mean(eval_drops)) if eval_drops else 0.0,
        "max_eval_drop": float(np.max(eval_drops)) if eval_drops else 0.0,
        "avg_move_time_ms": float(np.mean(move_times)) if move_times else 0.0,
        "opening_accuracy": 1.0 - (opening_blunders / max(len(opening_moves), 1)),
        "endgame_accuracy": 1.0 - (endgame_blunders / max(len(endgame_moves), 1)),
        "time_pressure_blunder_rate": (
            time_pressure_blunders / max(len(time_pressure_moves), 1)
        ),
        "total_moves": total_moves,
        "total_blunders": blunders,
        "total_mistakes": mistakes,
        "avg_eval": float(np.mean(eval_scores)) if eval_scores else 0.0,
    }

    return pd.DataFrame([features])


def _empty_features() -> dict[str, float]:
    return {
        "blunder_rate": 0.0,
        "mistake_rate": 0.0,
        "inaccuracy_rate": 0.0,
        "avg_eval_drop": 0.0,
        "max_eval_drop": 0.0,
        "avg_move_time_ms": 0.0,
        "opening_accuracy": 1.0,
        "endgame_accuracy": 1.0,
        "time_pressure_blunder_rate": 0.0,
        "total_moves": 0,
        "total_blunders": 0,
        "total_mistakes": 0,
        "avg_eval": 0.0,
    }
