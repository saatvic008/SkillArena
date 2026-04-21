import io
from datetime import datetime, timezone
from typing import Any

import chess
import chess.pgn


def parse_pgn_text(pgn_text: str) -> list[dict[str, Any]]:
    """Parse PGN text into structured game data with moves.
    
    Returns list of dicts, each containing game metadata and a list of moves.
    """
    games: list[dict[str, Any]] = []
    pgn_io = io.StringIO(pgn_text)

    while True:
        game = chess.pgn.read_game(pgn_io)
        if game is None:
            break

        headers = dict(game.headers)
        result_str = headers.get("Result", "*")
        result = _normalize_result(result_str, headers.get("White", ""))

        # Parse date
        date_str = headers.get("UTCDate", headers.get("Date", ""))
        played_at = _parse_date(date_str)

        # Extract moves
        moves = _extract_moves(game)

        game_data: dict[str, Any] = {
            "opponent": headers.get("Black", headers.get("White", "Unknown")),
            "result": result,
            "opening_name": headers.get("Opening", headers.get("ECO", "")),
            "opening_eco": headers.get("ECO", ""),
            "time_control": headers.get("TimeControl", ""),
            "played_at": played_at,
            "pgn_raw": str(game),
            "metadata": {
                "white": headers.get("White", ""),
                "black": headers.get("Black", ""),
                "site": headers.get("Site", ""),
                "event": headers.get("Event", ""),
            },
            "moves": moves,
        }
        games.append(game_data)

    return games


def _normalize_result(result_str: str, white_player: str) -> str:
    if result_str == "1-0":
        return "win"
    elif result_str == "0-1":
        return "loss"
    elif result_str == "1/2-1/2":
        return "draw"
    return "draw"


def _parse_date(date_str: str) -> datetime:
    for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return datetime.now(timezone.utc)


def _extract_moves(game: chess.pgn.Game) -> list[dict[str, Any]]:
    """Walk the game mainline and extract per-move data."""
    moves_data: list[dict[str, Any]] = []
    board = game.board()
    node = game

    move_number = 1
    for child_node in game.mainline():
        move = child_node.move
        fen_before = board.fen()
        san = board.san(move)
        uci = move.uci()
        color = "w" if board.turn == chess.WHITE else "b"

        board.push(move)
        fen_after = board.fen()

        # Extract eval from comments if available (Lichess format: [%eval 0.35])
        eval_score = _extract_eval(child_node.comment)

        # Heuristic blunder/mistake detection based on eval swings
        is_blunder = False
        is_mistake = False
        if eval_score is not None and len(moves_data) > 0:
            prev_eval = moves_data[-1].get("eval_score")
            if prev_eval is not None:
                delta = abs(eval_score - prev_eval)
                if delta >= 3.0:
                    is_blunder = True
                elif delta >= 1.5:
                    is_mistake = True

        move_data = {
            "move_number": move_number if color == "w" else move_number,
            "color": color,
            "san": san,
            "uci": uci,
            "fen_before": fen_before,
            "fen_after": fen_after,
            "eval_score": eval_score,
            "is_blunder": is_blunder,
            "is_mistake": is_mistake,
        }
        moves_data.append(move_data)

        if color == "b":
            move_number += 1

    return moves_data


def _extract_eval(comment: str) -> float | None:
    """Extract evaluation from PGN comment like [%eval 0.35] or [%eval #5]."""
    if not comment:
        return None
    import re
    match = re.search(r'\[%eval\s+([#\-\d.]+)\]', comment)
    if match:
        val = match.group(1)
        if val.startswith("#"):
            # Mate score: convert to large centipawn value
            try:
                mate_in = int(val[1:])
                return 100.0 if mate_in > 0 else -100.0
            except ValueError:
                return None
        try:
            return float(val)
        except ValueError:
            return None
    return None
