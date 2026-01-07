# app/schemas/completion.py
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CompletionCreate(BaseModel):
    done_on: date
    count: int = Field(ge=1, le=1000)
    notes: Optional[str] = Field(default=None, max_length=2000)


class CompletionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    done_on: date
    count: int
    notes: Optional[str] = None

