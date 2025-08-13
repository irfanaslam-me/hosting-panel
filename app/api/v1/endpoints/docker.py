"""
Docker management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db, User
from app.core.security import get_current_active_user
from app.services.docker_service import DockerService

router = APIRouter()


@router.get("/containers")
async def get_containers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all Docker containers"""
    docker_service = DockerService()
    return await docker_service.get_containers()


@router.get("/containers/{container_id}")
async def get_container(
    container_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific Docker container"""
    docker_service = DockerService()
    return await docker_service.get_container(container_id)


@router.post("/containers/{container_id}/start")
async def start_container(
    container_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start a Docker container"""
    docker_service = DockerService()
    result = await docker_service.start_container(container_id)
    
    if result["success"]:
        return {"message": f"Container {container_id} started successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.post("/containers/{container_id}/stop")
async def stop_container(
    container_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stop a Docker container"""
    docker_service = DockerService()
    result = await docker_service.stop_container(container_id)
    
    if result["success"]:
        return {"message": f"Container {container_id} stopped successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.post("/containers/{container_id}/restart")
async def restart_container(
    container_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Restart a Docker container"""
    docker_service = DockerService()
    result = await docker_service.restart_container(container_id)
    
    if result["success"]:
        return {"message": f"Container {container_id} restarted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.delete("/containers/{container_id}")
async def delete_container(
    container_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a Docker container"""
    docker_service = DockerService()
    result = await docker_service.delete_container(container_id)
    
    if result["success"]:
        return {"message": f"Container {container_id} deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.get("/images")
async def get_images(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all Docker images"""
    docker_service = DockerService()
    return await docker_service.get_images()


@router.post("/compose/up")
async def docker_compose_up(
    compose_file: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start Docker Compose services"""
    docker_service = DockerService()
    result = await docker_service.compose_up(compose_file)
    
    if result["success"]:
        return {"message": "Docker Compose services started successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )


@router.post("/compose/down")
async def docker_compose_down(
    compose_file: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stop Docker Compose services"""
    docker_service = DockerService()
    result = await docker_service.compose_down(compose_file)
    
    if result["success"]:
        return {"message": "Docker Compose services stopped successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        ) 