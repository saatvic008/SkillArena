import uuid
from datetime import date, datetime
from sqlalchemy import String, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class WeaknessReport(Base):
    __tablename__ = "weakness_reports"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    player_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    report_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    blunder_rate: Mapped[float | None] = mapped_column(Float)
    avg_accuracy: Mapped[float | None] = mapped_column(Float)
    weak_openings: Mapped[dict | None] = mapped_column(JSONB, default=list)
    weak_endgames: Mapped[dict | None] = mapped_column(JSONB, default=list)
    tactical_patterns: Mapped[dict | None] = mapped_column(JSONB, default=list)
    generated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    player = relationship("Player", back_populates="weakness_reports")
    recommendations = relationship("Recommendation", back_populates="report", lazy="selectin")
