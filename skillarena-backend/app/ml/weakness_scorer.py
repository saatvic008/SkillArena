import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from typing import Any

# Weakness profiles mapped to cluster centers
PROFILE_NAMES = ["Beginner", "Tactical", "Positional", "Time-pressure"]

# Pre-configured scaler and model (fit lazily on first call)
_scaler: MinMaxScaler | None = None
_kmeans: KMeans | None = None

FEATURE_COLS = [
    "blunder_rate", "inaccuracy_rate", "avg_eval_drop",
    "opening_accuracy", "endgame_accuracy", "time_pressure_blunder_rate",
]


def _fit_model() -> tuple[MinMaxScaler, KMeans]:
    """Fit KMeans on synthetic sample data representing 4 player profiles."""
    global _scaler, _kmeans

    # Synthetic training data representing different player archetypes
    sample_data = pd.DataFrame([
        # Beginners: high blunder rate, low accuracy everywhere
        {"blunder_rate": 0.15, "inaccuracy_rate": 0.30, "avg_eval_drop": 2.5,
         "opening_accuracy": 0.6, "endgame_accuracy": 0.5, "time_pressure_blunder_rate": 0.3},
        {"blunder_rate": 0.18, "inaccuracy_rate": 0.35, "avg_eval_drop": 3.0,
         "opening_accuracy": 0.55, "endgame_accuracy": 0.45, "time_pressure_blunder_rate": 0.35},
        {"blunder_rate": 0.20, "inaccuracy_rate": 0.38, "avg_eval_drop": 3.2,
         "opening_accuracy": 0.50, "endgame_accuracy": 0.40, "time_pressure_blunder_rate": 0.40},
        # Tactical weakness: decent openings but tactical blunders
        {"blunder_rate": 0.08, "inaccuracy_rate": 0.15, "avg_eval_drop": 1.5,
         "opening_accuracy": 0.85, "endgame_accuracy": 0.70, "time_pressure_blunder_rate": 0.10},
        {"blunder_rate": 0.10, "inaccuracy_rate": 0.18, "avg_eval_drop": 1.8,
         "opening_accuracy": 0.80, "endgame_accuracy": 0.65, "time_pressure_blunder_rate": 0.12},
        {"blunder_rate": 0.12, "inaccuracy_rate": 0.20, "avg_eval_drop": 2.0,
         "opening_accuracy": 0.78, "endgame_accuracy": 0.60, "time_pressure_blunder_rate": 0.15},
        # Positional weakness: good tactics but poor strategic play
        {"blunder_rate": 0.03, "inaccuracy_rate": 0.10, "avg_eval_drop": 0.8,
         "opening_accuracy": 0.70, "endgame_accuracy": 0.55, "time_pressure_blunder_rate": 0.05},
        {"blunder_rate": 0.04, "inaccuracy_rate": 0.12, "avg_eval_drop": 0.9,
         "opening_accuracy": 0.65, "endgame_accuracy": 0.50, "time_pressure_blunder_rate": 0.06},
        {"blunder_rate": 0.05, "inaccuracy_rate": 0.14, "avg_eval_drop": 1.0,
         "opening_accuracy": 0.60, "endgame_accuracy": 0.48, "time_pressure_blunder_rate": 0.08},
        # Time-pressure weakness: good normally, collapses under time
        {"blunder_rate": 0.04, "inaccuracy_rate": 0.08, "avg_eval_drop": 0.5,
         "opening_accuracy": 0.90, "endgame_accuracy": 0.85, "time_pressure_blunder_rate": 0.35},
        {"blunder_rate": 0.05, "inaccuracy_rate": 0.10, "avg_eval_drop": 0.6,
         "opening_accuracy": 0.88, "endgame_accuracy": 0.82, "time_pressure_blunder_rate": 0.40},
        {"blunder_rate": 0.03, "inaccuracy_rate": 0.07, "avg_eval_drop": 0.4,
         "opening_accuracy": 0.92, "endgame_accuracy": 0.88, "time_pressure_blunder_rate": 0.30},
    ])

    _scaler = MinMaxScaler()
    scaled = _scaler.fit_transform(sample_data[FEATURE_COLS])

    _kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    _kmeans.fit(scaled)

    return _scaler, _kmeans


def score_weaknesses(features_df: pd.DataFrame) -> dict[str, Any]:
    """Normalize features, predict cluster, and produce weakness scores 0-100."""
    global _scaler, _kmeans

    if _scaler is None or _kmeans is None:
        _fit_model()

    # Ensure we have the right columns, fill missing with 0
    for col in FEATURE_COLS:
        if col not in features_df.columns:
            features_df[col] = 0.0

    feature_values = features_df[FEATURE_COLS].values
    scaled = _scaler.transform(feature_values)
    cluster = _kmeans.predict(scaled)[0]
    profile_name = PROFILE_NAMES[cluster] if cluster < len(PROFILE_NAMES) else "Unknown"

    # Convert scaled values to 0-100 weakness scores (higher = worse)
    scores = scaled[0]
    weakness_scores = {
        "profile": profile_name,
        "cluster": int(cluster),
        "blunder_rate": float(features_df.iloc[0].get("blunder_rate", 0)),
        "avg_accuracy": float(1.0 - features_df.iloc[0].get("inaccuracy_rate", 0)) * 100,
        "scores": {
            "tactical": float(scores[0] * 100),       # blunder_rate
            "accuracy": float(scores[1] * 100),        # inaccuracy_rate
            "eval_control": float(scores[2] * 100),    # avg_eval_drop
            "opening": float((1 - scores[3]) * 100),   # opening_accuracy inverted
            "endgame": float((1 - scores[4]) * 100),   # endgame_accuracy inverted
            "time_pressure": float(scores[5] * 100),   # time_pressure_blunder_rate
        },
        "weak_openings": [
            {"name": "Opening preparation", "score": float((1 - scores[3]) * 100)}
        ],
        "weak_endgames": [
            {"name": "Endgame technique", "score": float((1 - scores[4]) * 100)}
        ],
        "tactical_patterns": [
            {"name": "Blunder avoidance", "score": float(scores[0] * 100)},
            {"name": "Time management", "score": float(scores[5] * 100)},
        ],
    }

    return weakness_scores
