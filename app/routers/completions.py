# app/routers/completions.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import date

from app.schemas.completion import CompletionCreate, CompletionRead
from app.services.completions import (
    CompletionStore,
    get_completion_store,
    HabitNotFoundError,
    CompletionAlreadyExistsError,
)

from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/habits/{habit_id}/completions", tags=["completions"])

# creates a new habit completion
@router.post("", response_model=CompletionRead, status_code=201) 
def create_completion(
    habit_id: int,
    completion_in: CompletionCreate,
    store: CompletionStore = Depends(get_completion_store),
    current_user: User = Depends(get_current_user),
):
    try:
        return store.create_completion(habit_id, completion_in, current_user.id)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")
    except CompletionAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Completion already exists")

# gets list of all completions for one habit
@router.get("", response_model=list[CompletionRead], response_model_exclude_none=True, status_code=200) 
def list_completions(
    habit_id: int,
    store: CompletionStore = Depends(get_completion_store),
    current_user: User = Depends(get_current_user),
):
    try:
        return store.list_completions(habit_id, current_user.id)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")

# toggles completion state for one habit
@router.post("/toggle/{for_date}") 
def toggle_completion(
    habit_id: int,
    for_date: date,
    store: CompletionStore = Depends(get_completion_store),
    current_user: User = Depends(get_current_user),
):
    try:
        completed = store.toggle_completion(habit_id, for_date, current_user.id)
        return {"completed": completed}
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")