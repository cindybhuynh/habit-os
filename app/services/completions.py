# app/services/completions.py
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.completion import HabitCompletion
from app.schemas.completion import CompletionCreate, CompletionRead


class HabitNotFoundError(Exception):
    pass


class CompletionStore:
    def __init__(self, db: Session):
        self.db = db

    def create_completion(self, habit_id: int, completion_in: CompletionCreate) -> CompletionRead:
        habit = self.db.get(Habit, habit_id)
        if habit is None:
            raise HabitNotFoundError()

        completion = HabitCompletion(
            habit_id=habit_id,
            **completion_in.model_dump(),
        )
        self.db.add(completion)
        self.db.commit()
        self.db.refresh(completion)
        return CompletionRead.model_validate(completion)

    def list_completions(self, habit_id: int) -> list[CompletionRead]:
        habit = self.db.get(Habit, habit_id)
        if habit is None:
            raise HabitNotFoundError()

        rows = (
            self.db.execute(
                select(HabitCompletion)
                .where(HabitCompletion.habit_id == habit_id)
                .order_by(HabitCompletion.done_on.desc(), HabitCompletion.id.desc())
            )
            .scalars()
            .all()
        )
        return [CompletionRead.model_validate(r) for r in rows]


def get_completion_store(db: Session = Depends(get_db)) -> CompletionStore:
    return CompletionStore(db)
