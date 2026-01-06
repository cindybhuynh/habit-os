# app/models/habit.py
from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Habit(Base):
    """
    ORM model representing the 'habits' table in PostgreSQL.
    """
    __tablename__ = "habits"

    __table_args__ = (
        CheckConstraint("target_count >= 1", name="ck_habits_target_count_ge1"),
        CheckConstraint("schedule_type IN ('daily', 'weekly')", name="ck_habits_schedule_type_valid"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    schedule_type: Mapped[str] = mapped_column(nullable=False)  # 'daily' or 'weekly'
    target_count: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(nullable=True)
