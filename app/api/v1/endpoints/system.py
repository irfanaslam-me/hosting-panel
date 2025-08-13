"""
System monitoring and management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db, User
from app.core.security import get_current_admin_user
from app.services.system_monitor import SystemMonitor

router = APIRouter()


@router.get("/status")
async def get_system_status(current_user: User = Depends(get_current_admin_user)):
    """Get system status and health"""
    monitor = SystemMonitor()
    return await monitor.get_system_status()


@router.get("/resources")
async def get_system_resources(current_user: User = Depends(get_current_admin_user)):
    """Get system resource usage"""
    monitor = SystemMonitor()
    return await monitor.get_resource_usage()


@router.get("/services")
async def get_services_status(current_user: User = Depends(get_current_admin_user)):
    """Get status of system services"""
    monitor = SystemMonitor()
    return await monitor.get_services_status()


@router.post("/services/{service_name}/restart")
async def restart_service(
    service_name: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Restart a system service"""
    monitor = SystemMonitor()
    result = await monitor.restart_service(service_name)
    
    if result["success"]:
        return {"message": f"Service {service_name} restarted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.get("/logs")
async def get_system_logs(
    service: str = None,
    lines: int = 100,
    current_user: User = Depends(get_current_admin_user)
):
    """Get system logs"""
    monitor = SystemMonitor()
    return await monitor.get_logs(service, lines)


@router.post("/backup")
async def create_system_backup(current_user: User = Depends(get_current_admin_user)):
    """Create a full system backup"""
    monitor = SystemMonitor()
    result = await monitor.create_system_backup()
    
    if result["success"]:
        return {"message": "System backup created successfully", "backup_path": result["backup_path"]}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.get("/updates")
async def check_updates(current_user: User = Depends(get_current_admin_user)):
    """Check for system updates"""
    monitor = SystemMonitor()
    return await monitor.check_updates()


@router.post("/updates")
async def install_updates(current_user: User = Depends(get_current_admin_user)):
    """Install system updates"""
    monitor = SystemMonitor()
    result = await monitor.install_updates()
    
    if result["success"]:
        return {"message": "System updates installed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        ) 