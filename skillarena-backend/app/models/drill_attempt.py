import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class DrillAttempt(Base):
    __tablename__ = "drill_attempts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    drill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("drills.id", ondelete="CASCADE"), nullable=False
    )
    player_move: Mapped[str] = mapped_column(String(10), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_taken_ms: Mapped[int | None] = mapped_column(Integer)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    player = relationship("Player", back_populates="drill_attempts")
    drill = relationship("Drill", back_populates="attempts")
