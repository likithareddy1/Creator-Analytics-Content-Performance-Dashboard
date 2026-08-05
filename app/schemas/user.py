from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# 👉 CREATE
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str


# 👉 UPDATE
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = None


# 👉 RESPONSE (VERY IMPORTANT 🔥)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True