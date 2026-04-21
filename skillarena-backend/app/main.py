from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.redis_client import close_redis
from app.utils.rate_limiter import limiter
from app.routers import auth, matches, analysis, drills, leaderboard, ws

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ML models are fit lazily on first use
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title="SkillArena API",
    description="AI-Powered Chess & Gaming Performance Analytics",
    version="1.0.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "status_code": 500},
    )


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(drills.router, prefix="/api/v1/drills", tags=["drills"])
app.include_router(leaderboard.router, prefix="/api/v1/leaderboard", tags=["leaderboard"])
app.include_router(ws.router, tags=["websocket"])


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": "skillarena"}
