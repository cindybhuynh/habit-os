# app/models/habit.py
from sqlalchemy import CheckConstraint, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Habit(Base):
    __tablename__ = "habits"

    __table_args__ = (
        CheckConstraint("target_count >= 1", name="ck_habits_target_count_ge1"),
        CheckConstraint("schedule_type IN ('daily', 'weekly')", name="ck_habits_schedule_type_valid"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    schedule_type: Mapped[str] = mapped_column(String(10), nullable=False)
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[object] = mapped_column(Date, nullable=False)  # date
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
