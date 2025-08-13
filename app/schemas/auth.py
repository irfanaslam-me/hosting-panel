"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None 