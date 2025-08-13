"""
Main API router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, websites, databases, system, docker, email

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(websites.router, prefix="/websites", tags=["websites"])
api_router.include_router(databases.router, prefix="/databases", tags=["databases"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(docker.router, prefix="/docker", tags=["docker"])
api_router.include_router(email.router, prefix="/email", tags=["email"]) 