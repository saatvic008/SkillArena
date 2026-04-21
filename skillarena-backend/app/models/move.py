import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from app.database import Base


class Move(Base):
    __tablename__ = "moves"
    __table_args__ = (
        CheckConstraint("color IN ('w', 'b')", name="ck_move_color"),
        {"postgresql_partition_by": "RANGE (created_at)"},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("matches.id"), nullable=False)
    move_number: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(1), nullable=False)
    san: Mapped[str] = mapped_column(String(10), nullable=False)
    uci: Mapped[str] = mapped_column(String(10), nullable=False)
    fen_before: Mapped[str] = mapped_column(Text, nullable=False)
    fen_after: Mapped[str] = mapped_column(Text, nullable=False)
    eval_score: Mapped[float | None] = mapped_column(Float)
    move_time_ms: Mapped[int | None] = mapped_column(Integer)
    is_blunder: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_mistake: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    match = relationship("Match", back_populates="moves", viewonly=True, primaryjoin="Match.id == foreign(Move.match_id)")
    annotations = relationship("MoveAnnotation", back_populates="move", lazy="selectin", primaryjoin="Move.id == foreign(MoveAnnotation.move_id)")
