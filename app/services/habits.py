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
from app.schemas.habit import HabitCreate, HabitRead, HabitReadWithStatus, HabitHistoryEntry
from app.services.completions import HabitNotFoundError


class HabitAlreadyExistsError(Exception):
    pass


class HabitStore:
    def __init__(self, db: Session):
        self.db = db

    def create_habit(self, habit_in: HabitCreate, user_id: int) -> HabitRead:
        habit = Habit(**habit_in.model_dump())
        habit.user_id = user_id
        self.db.add(habit)
        try:
            self.db.flush()
            self.db.refresh(habit)
            return HabitRead.model_validate(habit)
        except IntegrityError as e:
            self.db.rollback()
            raise HabitAlreadyExistsError() from e

    def get_habit(self, habit_id: int, user_id: int) -> HabitRead | None:
        habit = self.db.execute(
            select(Habit)
            .where(Habit.id == habit_id)
            .where(Habit.user_id == user_id)
        ).scalar_one_or_none()
        if habit is None:
            return None
        return HabitRead.model_validate(habit)

    def delete_habit(self, habit_id: int, user_id: int) -> bool:
        habit = self.db.execute(
            select(Habit)
            .where(Habit.id == habit_id)
            .where(Habit.user_id == user_id)
        ).scalar_one_or_none()
        if habit is None:
            return False
        self.db.delete(habit)
        self.db.flush()
        return True

    def list_habits_with_status(self, user_id: int, for_date: dt_date | None = None) -> list[HabitReadWithStatus]:
        if for_date is None:
            for_date = dt_date.today()

        habits = self.db.execute(
            select(Habit)
            .where(Habit.user_id == user_id)
            .order_by(Habit.id)
        ).scalars().all()

        completions = (
            self.db.execute(
                select(HabitCompletion)
                .join(Habit)
                .where(HabitCompletion.done_on == for_date)
                .where(Habit.user_id == user_id)
            ).scalars().all()
        )

        completion_map = {c.habit_id: c for c in completions}

        return [
            HabitReadWithStatus(
                **HabitRead.model_validate(h).model_dump(),
                completed_on_date=(h.id in completion_map),
                completion_count_on_date=completion_map[h.id].count if h.id in completion_map else 0,
                date=for_date,
            )
            for h in habits
        ]
    
    def get_habit_history(self, habit_id: int, user_id: int, start_date: dt_date, end_date: dt_date) -> list[HabitHistoryEntry]:
        
        habit = self.db.execute(
            select(Habit)
            .where(Habit.id == habit_id)
            .where(Habit.user_id == user_id)
        ).scalar_one_or_none()

        if habit is None:
            raise HabitNotFoundError()
        
        completions = self.db.execute(
            select(HabitCompletion)
            .where(HabitCompletion.habit_id == habit_id)
            .where(HabitCompletion.done_on >= start_date)
            .where(HabitCompletion.done_on <= end_date)
            .order_by(HabitCompletion.done_on)
        ).scalars().all()

        return [
            HabitHistoryEntry(date=c.done_on, count=c.count)
            for c in completions
        ]
    
def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)