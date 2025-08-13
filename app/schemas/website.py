"""
Website schemas
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class WebsiteBase(BaseModel):
    """Base website schema"""
    domain: str
    name: str
    type: str  # wordpress, php, static, python, docker
    php_version: Optional[str] = None


class WebsiteCreate(WebsiteBase):
    """Website creation schema"""
    ssl_enabled: bool = False
    document_root: Optional[str] = None


class WebsiteUpdate(BaseModel):
    """Website update schema"""
    name: Optional[str] = None
    status: Optional[str] = None  # active, inactive, suspended
    php_version: Optional[str] = None
    ssl_enabled: Optional[bool] = None


class WebsiteResponse(WebsiteBase):
    """Website response schema"""
    id: int
    status: str
    document_root: str
    ssl_enabled: bool
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True


class WebsiteStats(BaseModel):
    """Website statistics schema"""
    disk_usage: int  # bytes
    bandwidth_usage: int  # bytes
    requests_per_day: int
    uptime_percentage: float
    last_backup: Optional[datetime] = None


class WebsiteList(BaseModel):
    """Website list response schema"""
    websites: List[WebsiteResponse]
    total: int
    page: int
    per_page: int 