from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.player import Player
from app.schemas.auth import (
    PlayerCreate, PlayerLogin, PlayerResponse, TokenResponse, RefreshRequest,
)
from app.utils.auth_utils import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.utils.rate_limiter import limiter

router = APIRouter()


@router.post("/register", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute")
async def register(
    request: Request,
    body: PlayerCreate,
    db: AsyncSession = Depends(get_db),
) -> PlayerResponse:
    existing = await db.execute(
        select(Player).where(
            (Player.username == body.username) | (Player.email == body.email)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered",
        )

    player = Player(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(player)
    await db.flush()
    await db.refresh(player)
    return PlayerResponse.model_validate(player)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("60/minute")
async def login(
    request: Request,
    body: PlayerLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    result = await db.execute(
        select(Player).where(Player.username == body.username)
    )
    player = result.scalar_one_or_none()
    if not player or not verify_password(body.password, player.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token({"sub": str(player.id)})
    refresh_token = create_refresh_token({"sub": str(player.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("60/minute")
async def refresh_token(
    request: Request,
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type — expected refresh token",
        )
    player_id = payload.get("sub")
    result = await db.execute(
        select(Player).where(Player.id == player_id)
    )
    player = result.scalar_one_or_none()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Player not found",
        )

    access_token = create_access_token({"sub": str(player.id)})
    new_refresh = create_refresh_token({"sub": str(player.id)})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh)
