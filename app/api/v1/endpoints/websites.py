"""
Website management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db, User, Website
from app.core.security import get_current_active_user, get_current_admin_user
from app.schemas.website import (
    WebsiteCreate, WebsiteUpdate, WebsiteResponse, WebsiteList, WebsiteStats
)
from app.services.website_service import WebsiteService
from app.services.ssl_service import SSLService

router = APIRouter()


@router.post("/", response_model=WebsiteResponse)
async def create_website(
    website_data: WebsiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new website"""
    # Check if domain already exists
    existing_website = db.query(Website).filter(Website.domain == website_data.domain).first()
    if existing_website:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Domain already exists"
        )
    
    # Create website using service
    website_service = WebsiteService(db)
    website = await website_service.create_website(website_data, current_user.id)
    
    return website


@router.get("/", response_model=WebsiteList)
async def get_websites(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get websites with pagination"""
    query = db.query(Website)
    
    # Filter by user if not admin
    if not current_user.is_admin:
        query = query.filter(Website.owner_id == current_user.id)
    
    total = query.count()
    websites = query.offset(skip).limit(limit).all()
    
    return WebsiteList(
        websites=websites,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )


@router.get("/{website_id}", response_model=WebsiteResponse)
async def get_website(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return website


@router.put("/{website_id}", response_model=WebsiteResponse)
async def update_website(
    website_id: int,
    website_data: WebsiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update website using service
    website_service = WebsiteService(db)
    updated_website = await website_service.update_website(website_id, website_data)
    
    return updated_website


@router.delete("/{website_id}")
async def delete_website(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Delete website using service
    website_service = WebsiteService(db)
    await website_service.delete_website(website_id)
    
    return {"message": "Website deleted successfully"}


@router.post("/{website_id}/ssl")
async def install_ssl(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Install SSL certificate for a website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Install SSL using service
    ssl_service = SSLService(db)
    result = await ssl_service.install_ssl(website.domain)
    
    return {"message": "SSL certificate installed successfully", "details": result}


@router.get("/{website_id}/stats", response_model=WebsiteStats)
async def get_website_stats(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get website statistics"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get stats using service
    website_service = WebsiteService(db)
    stats = await website_service.get_website_stats(website_id)
    
    return stats


@router.post("/{website_id}/backup")
async def create_backup(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a backup of the website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create backup using service
    website_service = WebsiteService(db)
    backup = await website_service.create_backup(website_id)
    
    return {"message": "Backup created successfully", "backup_id": backup.id}


@router.post("/{website_id}/restart")
async def restart_website(
    website_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Restart a website"""
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Website not found"
        )
    
    # Check permissions
    if not current_user.is_admin and website.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Restart website using service
    website_service = WebsiteService(db)
    await website_service.restart_website(website_id)
    
    return {"message": "Website restarted successfully"} 