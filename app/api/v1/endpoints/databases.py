"""
Database management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db, User, Database
from app.core.security import get_current_active_user
from app.schemas.database import (
    DatabaseCreate, DatabaseUpdate, DatabaseResponse, DatabaseList
)
from app.services.database_service import DatabaseService

router = APIRouter()


@router.post("/", response_model=DatabaseResponse)
async def create_database(
    database_data: DatabaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new database"""
    # Check if database name already exists
    existing_database = db.query(Database).filter(Database.name == database_data.name).first()
    if existing_database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database name already exists"
        )
    
    # Create database using service
    database_service = DatabaseService(db)
    database = await database_service.create_database(database_data)
    
    return database


@router.get("/", response_model=DatabaseList)
async def get_databases(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get databases with pagination"""
    query = db.query(Database)
    
    # Filter by user if not admin
    if not current_user.is_admin:
        # Get user's websites and their databases
        user_websites = db.query(Website).filter(Website.owner_id == current_user.id).all()
        website_ids = [website.id for website in user_websites]
        query = query.filter(Database.website_id.in_(website_ids))
    
    total = query.count()
    databases = query.offset(skip).limit(limit).all()
    
    return DatabaseList(
        databases=databases,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )


@router.get("/{database_id}", response_model=DatabaseResponse)
async def get_database(
    database_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific database"""
    database = db.query(Database).filter(Database.id == database_id).first()
    if not database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database not found"
        )
    
    # Check permissions
    if not current_user.is_admin:
        website = db.query(Website).filter(Website.id == database.website_id).first()
        if not website or website.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return database


@router.put("/{database_id}", response_model=DatabaseResponse)
async def update_database(
    database_id: int,
    database_data: DatabaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a database"""
    database = db.query(Database).filter(Database.id == database_id).first()
    if not database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database not found"
        )
    
    # Check permissions
    if not current_user.is_admin:
        website = db.query(Website).filter(Website.id == database.website_id).first()
        if not website or website.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Update database using service
    database_service = DatabaseService(db)
    updated_database = await database_service.update_database(database_id, database_data)
    
    return updated_database


@router.delete("/{database_id}")
async def delete_database(
    database_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a database"""
    database = db.query(Database).filter(Database.id == database_id).first()
    if not database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database not found"
        )
    
    # Check permissions
    if not current_user.is_admin:
        website = db.query(Website).filter(Website.id == database.website_id).first()
        if not website or website.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Delete database using service
    database_service = DatabaseService(db)
    await database_service.delete_database(database_id)
    
    return {"message": "Database deleted successfully"}


@router.post("/{database_id}/backup")
async def create_database_backup(
    database_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a backup of the database"""
    database = db.query(Database).filter(Database.id == database_id).first()
    if not database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database not found"
        )
    
    # Check permissions
    if not current_user.is_admin:
        website = db.query(Website).filter(Website.id == database.website_id).first()
        if not website or website.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Create backup using service
    database_service = DatabaseService(db)
    backup = await database_service.create_backup(database_id)
    
    return {"message": "Database backup created successfully", "backup_id": backup.id}


# Import at the end to avoid circular imports
from app.core.database import Website 