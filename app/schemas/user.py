<<<<<<< HEAD
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
=======
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema containing shared user attributes."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating/registering a new user."""
    password: str


# Alias for backward compatibility if code uses UserRegister
UserRegister = UserCreate


class UserUpdate(BaseModel):
    """Schema for updating user details (all fields optional)."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for returning user data (excludes sensitive info)."""
    
    class Config:
        from_attributes = True  # Supports ORM models (FastAPI v2 / Pydantic v2)


class UserInDB(UserBase):
    """Internal schema representing user in database with hashed password."""
    hashed_password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data stored within JWT token."""
    username: Optional[str] = None
>>>>>>> 567a2ff61666ec1d3b961045a6a013fac9a11976
