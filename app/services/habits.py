# app/services/habits.py
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitRead

class HabitStore:
    def __init__(self, db: Session):
        self.db = db

    def create_habit(self, habit_in: HabitCreate) -> HabitRead:
        habit = Habit(**habit_in.model_dump())
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return HabitRead.model_validate(habit)

    def list_habits(self) -> list[HabitRead]:
        habits = self.db.execute(select(Habit).order_by(Habit.id)).scalars().all()
        return [HabitRead.model_validate(h) for h in habits]

    def get_habit(self, habit_id: int) -> HabitRead | None:
        habit = self.db.get(Habit, habit_id)
        return HabitRead.model_validate(habit) if habit else None

def get_store(db: Session = Depends(get_db)) -> HabitStore:
    return HabitStore(db)
