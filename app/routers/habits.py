#app/routers/habits.py
from datetime import date as dt_date
from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.habit import HabitCreate, HabitRead, HabitReadWithStatus
from app.services.habits import HabitStore, get_store, HabitAlreadyExistsError

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("", response_model=HabitRead, status_code=201)
def create_habit(habit_in: HabitCreate, store: HabitStore = Depends(get_store)):
    try:
        return store.create_habit(habit_in)
    except HabitAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Habit already exists")


@router.get("", response_model=list[HabitRead] | list[HabitReadWithStatus], response_model_exclude_none=True)
def list_habits(
    store: HabitStore = Depends(get_store),
    include_status: bool = Query(False, description="Include completion status for a given date"),
    for_date: dt_date | None = Query(None, description="Date to compute completion status for (defaults to today)"),
):
    # If not requested, return the plain habits list
    if not include_status:
        return store.list_habits()

    return store.list_habits_with_status(for_date=for_date)


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, store: HabitStore = Depends(get_store)):
    habit = store.get_habit(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: int, store: HabitStore = Depends(get_store)):
    if not store.delete_habit(habit_id):
        raise HTTPException(status_code=404, detail="Habit not found")
    return None
