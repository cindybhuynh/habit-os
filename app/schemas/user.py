# app/schemas/user.py
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    
class UserRead(BaseModel): 
    model_config = ConfigDict(from_attributes=True) # connects schema to ORM models

    id: int
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"