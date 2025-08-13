"""
Email management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db, User, EmailAccount
from app.core.security import get_current_active_user
from app.services.email_service import EmailService

router = APIRouter()


@router.get("/accounts")
async def get_email_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get email accounts"""
    query = db.query(EmailAccount)
    
    # Filter by user if not admin
    if not current_user.is_admin:
        query = query.filter(EmailAccount.owner_id == current_user.id)
    
    accounts = query.all()
    return accounts


@router.post("/accounts")
async def create_email_account(
    email: str,
    password: str,
    domain: str,
    quota: int = 1000,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new email account"""
    # Check if email already exists
    existing_account = db.query(EmailAccount).filter(EmailAccount.email == email).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email account already exists"
        )
    
    # Create email account using service
    email_service = EmailService(db)
    account = await email_service.create_email_account(email, password, domain, quota, current_user.id)
    
    return account


@router.delete("/accounts/{account_id}")
async def delete_email_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an email account"""
    account = db.query(EmailAccount).filter(EmailAccount.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email account not found"
        )
    
    # Check permissions
    if not current_user.is_admin and account.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Delete email account using service
    email_service = EmailService(db)
    await email_service.delete_email_account(account_id)
    
    return {"message": "Email account deleted successfully"}


@router.post("/setup")
async def setup_email_server(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Setup email server (Postfix + Dovecot)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    email_service = EmailService(db)
    result = await email_service.setup_email_server()
    
    if result["success"]:
        return {"message": "Email server setup completed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.get("/status")
async def get_email_server_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get email server status"""
    email_service = EmailService(db)
    return await email_service.get_server_status() 