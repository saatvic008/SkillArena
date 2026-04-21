import uuid
from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    report_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("weakness_reports.id", ondelete="CASCADE"), nullable=False
    )
    drill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("drills.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    player = relationship("Player", back_populates="recommendations")
    report = relationship("WeaknessReport", back_populates="recommendations")
    drill = relationship("Drill", back_populates="recommendations")
