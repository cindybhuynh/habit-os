# app/models/completion.py
from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    __table_args__ = (
        CheckConstraint("count >= 1", name="ck_habit_completions_count_ge1"),
        UniqueConstraint("habit_id", "done_on", name="uq_completion_habit_day"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    done_on: Mapped[date] = mapped_column(nullable=False, index=True)
    count: Mapped[int] = mapped_column(nullable=False, default=1)
    notes: Mapped[str | None] = mapped_column(nullable=True)

__table_args__ = (
    CheckConstraint("count >= 1", name="ck_habit_completions_count_ge1"),
    UniqueConstraint("habit_id", "done_on", name="uq_completion_habit_day"),
)