import uuid
from sqlalchemy import String, Integer, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Drill(Base):
    __tablename__ = "drills"
    __table_args__ = (
        CheckConstraint("difficulty BETWEEN 1 AND 5", name="ck_drill_difficulty"),
        CheckConstraint("category IN ('tactic', 'endgame', 'opening')", name="ck_drill_category"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    fen_position: Mapped[str] = mapped_column(Text, nullable=False)
    correct_move: Mapped[str] = mapped_column(String(10), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)

    attempts = relationship("DrillAttempt", back_populates="drill", lazy="selectin")
    recommendations = relationship("Recommendation", back_populates="drill", lazy="selectin")
