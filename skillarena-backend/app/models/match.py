import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from app.database import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("source IN ('lichess', 'chesscom', 'upload')", name="ck_match_source"),
        CheckConstraint("result IN ('win', 'loss', 'draw')", name="ck_match_result"),
        {"postgresql_partition_by": "RANGE (played_at)"},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    opponent_username: Mapped[str | None] = mapped_column(String(100))
    result: Mapped[str] = mapped_column(String(10), nullable=False)
    opening_name: Mapped[str | None] = mapped_column(String(200))
    opening_eco: Mapped[str | None] = mapped_column(String(10))
    time_control: Mapped[str | None] = mapped_column(String(30))
    played_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    pgn_raw: Mapped[str | None] = mapped_column(Text)
    match_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)

    player = relationship("Player", back_populates="matches")
    moves = relationship("Move", back_populates="match", lazy="selectin", primaryjoin="Match.id == foreign(Move.match_id)")
