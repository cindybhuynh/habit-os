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
        if for_date is None:
            for_date = dt_date.today()

        stmt = (
            select(Habit, HabitCompletion)
            .outerjoin(
                HabitCompletion,
                (HabitCompletion.habit_id == Habit.id) & (HabitCompletion.done_on == for_date),
            )
            .order_by(Habit.id)
        )

        rows = self.db.execute(stmt).all()

        results: list[HabitReadWithStatus] = []
        for habit, completion in rows:
            results.append(
                HabitReadWithStatus(
                    id=habit.id,
                    name=habit.name,
                    schedule_type=habit.schedule_type,
                    target_count=habit.target_count,
                    start_date=habit.start_date,
                    notes=habit.notes,
                    completed_on_date=(completion is not None),
                    completion_count_on_date=(completion.count if completion is not None else 0),
                    date=for_date,
                )
            )
        return results


def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)
