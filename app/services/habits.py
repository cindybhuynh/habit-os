# app/services/habits.py
from __future__ import annotations

from datetime import date as dt_date
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.completion import HabitCompletion
from app.schemas.habit import HabitCreate, HabitRead, HabitReadWithStatus


class HabitAlreadyExistsError(Exception):
    pass


class HabitStore:
    """
    Service layer for Habit operations (DB logic only).
    """
    def __init__(self, db: Session):
        self.db = db

    def create_habit(self, habit_in: HabitCreate) -> HabitRead:
        habit = Habit(**habit_in.model_dump())
        self.db.add(habit)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HabitAlreadyExistsError() from e

        self.db.refresh(habit)
        return HabitRead.model_validate(habit)

    def list_habits(self) -> list[HabitRead]:
        habits = self.db.execute(select(Habit).order_by(Habit.id)).scalars().all()
        return [HabitRead.model_validate(h) for h in habits]

    def get_habit(self, habit_id: int) -> HabitRead | None:
        habit = self.db.get(Habit, habit_id)
        return HabitRead.model_validate(habit) if habit else None

    def delete_habit(self, habit_id: int) -> bool:
        habit = self.db.get(Habit, habit_id)
        if habit is None:
            return False

        self.db.delete(habit)
        self.db.commit()
        return True

    def list_habits_with_status(self, for_date: dt_date | None = None) -> list[HabitReadWithStatus]:
        """
        Returns habits enriched with completion status for the given date.
        One completion per habit per day => completion_count_on_date is 0 or 1.
        """
        day = for_date or dt_date.today()

        # Load all habits
        habits = self.db.execute(select(Habit).order_by(Habit.id)).scalars().all()
        if not habits:
            return []

        habit_ids = [h.id for h in habits]

        # Fetch completions for that day for these habits
        completed_ids = set(
            self.db.execute(
                select(HabitCompletion.habit_id)
                .where(HabitCompletion.done_on == day)
                .where(HabitCompletion.habit_id.in_(habit_ids))
            ).scalars().all()
        )

        # Build response objects
        result: list[HabitReadWithStatus] = []
        for h in habits:
            done = h.id in completed_ids
            result.append(
                HabitReadWithStatus(
                    id=h.id,
                    name=h.name,
                    schedule_type=h.schedule_type,
                    target_count=h.target_count,
                    start_date=h.start_date,
                    notes=h.notes,
                    completed_on_date=done,
                    completion_count_on_date=1 if done else 0,
                    date=day,
                )
            )
        return result


def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)
