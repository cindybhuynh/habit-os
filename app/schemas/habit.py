from datetime import date 
from typing import Optional, Literal
from pydantic import BaseModel, Field

class HabitCreate(BaseModel):
    name: str = Field(min_length=1)
    schedule_type: Literal["daily", "weekly"]
    target_count: int = Field(ge=1) # ge = greater than or equal to
    start_date: date
    notes: Optional[str] = None

class HabitRead(BaseModel): 
    id: int
    name: str
    schedule_type: Literal["daily", "weekly"]
    target_count: int
    start_date: date
    notes: Optional[str] = None