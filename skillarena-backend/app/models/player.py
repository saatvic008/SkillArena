import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    elo_rating: Mapped[int] = mapped_column(Integer, default=1200, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    matches = relationship("Match", back_populates="player", lazy="selectin")
    weakness_reports = relationship("WeaknessReport", back_populates="player", lazy="selectin")
    drill_attempts = relationship("DrillAttempt", back_populates="player", lazy="selectin")
    recommendations = relationship("Recommendation", back_populates="player", lazy="selectin")
