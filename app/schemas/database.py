"""
Database schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DatabaseBase(BaseModel):
    """Base database schema"""
    name: str
    type: str = "mysql"  # mysql, postgresql


class DatabaseCreate(DatabaseBase):
    """Database creation schema"""
    username: str
    password: str


class DatabaseUpdate(BaseModel):
    """Database update schema"""
    password: Optional[str] = None
    status: Optional[str] = None  # active, inactive


class DatabaseResponse(DatabaseBase):
    """Database response schema"""
    id: int
    username: str
    status: str
    created_at: datetime
    website_id: int
    
    class Config:
        from_attributes = True


class DatabaseStats(BaseModel):
    """Database statistics schema"""
    size: int  # bytes
    tables_count: int
    connections: int
    queries_per_second: float
    last_backup: Optional[datetime] = None


class DatabaseList(BaseModel):
    """Database list response schema"""
    databases: List[DatabaseResponse]
    total: int
    page: int
    per_page: int 