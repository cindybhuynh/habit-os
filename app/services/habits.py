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
    def __init__(self, db: Session):
        self.db = db

    def create_habit(self, habit_in: HabitCreate) -> HabitRead:
        # 1. Use model_dump() but be careful with ID/Relationship fields if they existed
        habit = Habit(**habit_in.model_dump())
        self.db.add(habit)
        try:
            self.db.commit()
            self.db.refresh(habit) 
            return HabitRead.model_validate(habit)
        except IntegrityError as e:
            self.db.rollback() # Crucial: Clean up the 'failed' transaction
            raise HabitAlreadyExistsError() from e

    def list_habits_with_status(self, for_date: dt_date | None = None) -> list[HabitReadWithStatus]:
        if for_date is None:
            for_date = dt_date.today()

        # 2. Optimization: The "N+1" Problem
        # Currently, you fetch ALL habits, then ALL completions. 
        # This works for now, but in the future, we'd use a JOIN.
        habits = self.db.execute(select(Habit).order_by(Habit.id)).scalars().all()

        completions = (
            self.db.execute(
                select(HabitCompletion).where(HabitCompletion.done_on == for_date)
            ).scalars().all()
        )

        completion_map = {c.habit_id: c for c in completions}

        # 3. Use model_validate for status too (cleaner)
        return [
            HabitReadWithStatus(
                **HabitRead.model_validate(h).model_dump(), # Copy base habit data
                completed_on_date=(h.id in completion_map),
                completion_count_on_date=completion_map[h.id].count if h.id in completion_map else 0,
                date=for_date,
            )
            for h in habits
        ]


def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)
