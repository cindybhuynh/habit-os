from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

class HabitCreate(BaseModel):
    name: str = Field(min_length=1)
    schedule_type: Literal["daily", "weekly"]
    target_count: int = Field(ge=1)
    start_date: date
    notes: Optional[str] = None

class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    schedule_type: Literal["daily", "weekly"]
    target_count: int
    start_date: date
    notes: Optional[str] = None
# Note: You can add HabitUpdate later if you want to support updating habits.