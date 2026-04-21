import uuid
from sqlalchemy import String, Float, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from app.database import Base


class MoveAnnotation(Base):
    __tablename__ = "move_annotations"
    __table_args__ = (
        CheckConstraint(
            "annotation_type IN ('blunder', 'inaccuracy', 'best_move', 'brilliant')",
            name="ck_annotation_type",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    move_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("moves.id"), nullable=False)
    annotation_type: Mapped[str] = mapped_column(String(20), nullable=False)
    engine_best_move: Mapped[str | None] = mapped_column(String(10))
    eval_delta: Mapped[float | None] = mapped_column(Float)
    annotation_text: Mapped[str | None] = mapped_column(Text)
    move = relationship("Move", back_populates="annotations", viewonly=True, primaryjoin="Move.id == foreign(MoveAnnotation.move_id)")
