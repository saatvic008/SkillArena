import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PlayerCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class PlayerLogin(BaseModel):
    username: str
    password: str


class PlayerResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    elo_rating: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
