#app/schemas/habit.py
from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    schedule_type: Literal["daily", "weekly"]
    target_count: int = Field(ge=1, le=1000)
    start_date: date
    notes: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be blank")
        return v


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    schedule_type: Literal["daily", "weekly"]
    target_count: int
    start_date: date
    notes: Optional[str] = None

class HabitReadWithStatus(HabitRead):
    completed_on_date: bool
    completion_count_on_date: int
    date: date
