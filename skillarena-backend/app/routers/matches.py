import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, BackgroundTasks, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.player import Player
from app.models.match import Match
from app.models.move import Move
from app.schemas.match import (
    MatchResponse, MatchListResponse, MatchDetailResponse,
    FetchLichessRequest, FetchChesscomRequest, MoveInMatch,
)
from app.utils.auth_utils import get_current_player
from app.utils.rate_limiter import limiter
from app.services.pgn_parser import parse_pgn_text
from app.services.lichess import fetch_lichess_games
from app.services.chesscom import fetch_chesscom_games
from app.config import get_settings

settings = get_settings()
router = APIRouter()

ALLOWED_EXTENSIONS = {".pgn", ".json"}
MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@router.post("/upload", response_model=MatchListResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("200/minute")
async def upload_pgn(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> MatchListResponse:
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {ALLOWED_EXTENSIONS} files are accepted",
        )

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit",
        )

    pgn_text = content.decode("utf-8", errors="replace")
    parsed_games = parse_pgn_text(pgn_text)

    created_matches: list[Match] = []
    for game_data in parsed_games:
        match = Match(
            player_id=player.id,
            source="upload",
            opponent_username=game_data.get("opponent"),
            result=game_data.get("result", "draw"),
            opening_name=game_data.get("opening_name"),
            opening_eco=game_data.get("opening_eco"),
            time_control=game_data.get("time_control"),
            played_at=game_data.get("played_at"),
            pgn_raw=game_data.get("pgn_raw"),
            match_metadata=game_data.get("metadata", {}),
        )
        db.add(match)
        await db.flush()
        await db.refresh(match)

        for move_data in game_data.get("moves", []):
            move = Move(
                match_id=match.id,
                move_number=move_data["move_number"],
                color=move_data["color"],
                san=move_data["san"],
                uci=move_data["uci"],
                fen_before=move_data["fen_before"],
                fen_after=move_data["fen_after"],
                eval_score=move_data.get("eval_score"),
                is_blunder=move_data.get("is_blunder", False),
                is_mistake=move_data.get("is_mistake", False),
            )
            db.add(move)

        created_matches.append(match)

    return MatchListResponse(
        matches=[MatchResponse.model_validate(m) for m in created_matches],
        total=len(created_matches),
    )


@router.post("/fetch/lichess", response_model=MatchListResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("200/minute")
async def fetch_from_lichess(
    request: Request,
    body: FetchLichessRequest,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> MatchListResponse:
    pgn_text = await fetch_lichess_games(body.lichess_username, body.max_games)
    if not pgn_text:
        raise HTTPException(status_code=404, detail="No games found on Lichess")

    parsed_games = parse_pgn_text(pgn_text)
    created_matches: list[Match] = []
    for game_data in parsed_games:
        match = Match(
            player_id=player.id,
            source="lichess",
            opponent_username=game_data.get("opponent"),
            result=game_data.get("result", "draw"),
            opening_name=game_data.get("opening_name"),
            opening_eco=game_data.get("opening_eco"),
            time_control=game_data.get("time_control"),
            played_at=game_data.get("played_at"),
            pgn_raw=game_data.get("pgn_raw"),
            match_metadata=game_data.get("metadata", {}),
        )
        db.add(match)
        await db.flush()
        await db.refresh(match)

        for move_data in game_data.get("moves", []):
            move = Move(
                match_id=match.id,
                move_number=move_data["move_number"],
                color=move_data["color"],
                san=move_data["san"],
                uci=move_data["uci"],
                fen_before=move_data["fen_before"],
                fen_after=move_data["fen_after"],
                eval_score=move_data.get("eval_score"),
                is_blunder=move_data.get("is_blunder", False),
                is_mistake=move_data.get("is_mistake", False),
            )
            db.add(move)

        created_matches.append(match)

    return MatchListResponse(
        matches=[MatchResponse.model_validate(m) for m in created_matches],
        total=len(created_matches),
    )


@router.post("/fetch/chesscom", response_model=MatchListResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("200/minute")
async def fetch_from_chesscom(
    request: Request,
    body: FetchChesscomRequest,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> MatchListResponse:
    pgn_text = await fetch_chesscom_games(body.chesscom_username, body.year, body.month)
    if not pgn_text:
        raise HTTPException(status_code=404, detail="No games found on Chess.com")

    parsed_games = parse_pgn_text(pgn_text)
    created_matches: list[Match] = []
    for game_data in parsed_games:
        match = Match(
            player_id=player.id,
            source="chesscom",
            opponent_username=game_data.get("opponent"),
            result=game_data.get("result", "draw"),
            opening_name=game_data.get("opening_name"),
            opening_eco=game_data.get("opening_eco"),
            time_control=game_data.get("time_control"),
            played_at=game_data.get("played_at"),
            pgn_raw=game_data.get("pgn_raw"),
            match_metadata=game_data.get("metadata", {}),
        )
        db.add(match)
        await db.flush()
        await db.refresh(match)

        for move_data in game_data.get("moves", []):
            move = Move(
                match_id=match.id,
                move_number=move_data["move_number"],
                color=move_data["color"],
                san=move_data["san"],
                uci=move_data["uci"],
                fen_before=move_data["fen_before"],
                fen_after=move_data["fen_after"],
                eval_score=move_data.get("eval_score"),
                is_blunder=move_data.get("is_blunder", False),
                is_mistake=move_data.get("is_mistake", False),
            )
            db.add(move)

        created_matches.append(match)

    return MatchListResponse(
        matches=[MatchResponse.model_validate(m) for m in created_matches],
        total=len(created_matches),
    )


@router.get("", response_model=MatchListResponse)
@limiter.limit("200/minute")
async def list_matches(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> MatchListResponse:
    count_result = await db.execute(
        select(func.count(Match.id)).where(Match.player_id == player.id)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Match)
        .where(Match.player_id == player.id)
        .order_by(Match.played_at.desc())
        .offset(skip)
        .limit(limit)
    )
    matches = result.scalars().all()
    return MatchListResponse(
        matches=[MatchResponse.model_validate(m) for m in matches],
        total=total,
    )


@router.get("/{match_id}", response_model=MatchDetailResponse)
@limiter.limit("200/minute")
async def get_match(
    request: Request,
    match_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    player: Player = Depends(get_current_player),
) -> MatchDetailResponse:
    result = await db.execute(
        select(Match).where(Match.id == match_id, Match.player_id == player.id)
    )
    match = result.scalar_one_or_none()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    moves_result = await db.execute(
        select(Move)
        .where(Move.match_id == match_id)
        .order_by(Move.move_number, Move.color)
    )
    moves = moves_result.scalars().all()

    return MatchDetailResponse(
        id=match.id,
        source=match.source,
        opponent_username=match.opponent_username,
        result=match.result,
        opening_name=match.opening_name,
        opening_eco=match.opening_eco,
        time_control=match.time_control,
        played_at=match.played_at,
        pgn_raw=match.pgn_raw,
        metadata=match.match_metadata,
        moves=[MoveInMatch.model_validate(m) for m in moves],
    )
