#app/routers/habits.py
from datetime import date as dt_date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.habit import HabitCreate, HabitRead, HabitReadWithStatus, HabitHistoryEntry
from app.services.habits import HabitStore, get_store, HabitAlreadyExistsError
from app.services.completions import HabitNotFoundError

from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/habits", tags=["habits"])

# creates new habit
@router.post("", response_model=HabitRead, status_code=201)
def create_habit(habit_in: HabitCreate, store: HabitStore = Depends(get_store), current_user: User = Depends(get_current_user)):
    try:
        return store.create_habit(habit_in, current_user.id)
    except HabitAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Habit already exists")

# gets list of habits
@router.get("", response_model=list[HabitReadWithStatus], response_model_exclude_none=True)
def list_habits(store: HabitStore = Depends(get_store), current_user: User = Depends(get_current_user)):
    return store.list_habits_with_status(current_user.id)

# gets list of habits based on date
@router.get("/status", response_model=list[HabitReadWithStatus], response_model_exclude_none=True)
def list_habits_status(
    store: HabitStore = Depends(get_store),
    current_user: User = Depends(get_current_user),
    for_date: dt_date | None = Query(None, description="Date to compute completion status for (defaults to today)"),
):
    return store.list_habits_with_status(current_user.id, for_date=for_date)

# gets habit based on habit id
@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, store: HabitStore = Depends(get_store), current_user: User = Depends(get_current_user)):
    habit = store.get_habit(habit_id, current_user.id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

# deletes habit based on habit id
@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: int, store: HabitStore = Depends(get_store), current_user: User = Depends(get_current_user)):
    if not store.delete_habit(habit_id, current_user.id):
        raise HTTPException(status_code=404, detail="Habit not found")
    return None

# gets habit history based on habit id
@router.get("/{habit_id}/history", response_model=list[HabitHistoryEntry])
def get_habit_history(
    habit_id: int, 
    store: HabitStore = Depends(get_store), 
    current_user: User = Depends(get_current_user), 
    start_date: dt_date = Query(default_factory=lambda: dt_date.today() - timedelta(days=365)), 
    end_date: dt_date = Query(default_factory=dt_date.today)
):
    try:
        return store.get_habit_history(habit_id, current_user.id, start_date, end_date)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")