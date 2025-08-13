#!/usr/bin/env python3
"""
Modern Hosting Panel - Main Application
A lightweight, modern web-based hosting panel for managing websites and services.
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router
from app.core.security import create_admin_user
from app.services.system_monitor import SystemMonitor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Modern Hosting Panel...")
    
    # Initialize database
    await init_db()
    
    # Create admin user if not exists
    await create_admin_user()
    
    # Start system monitoring
    SystemMonitor.start()
    
    print("✅ Modern Hosting Panel is ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Modern Hosting Panel...")
    SystemMonitor.stop()


# Create FastAPI application
app = FastAPI(
    title="Modern Hosting Panel",
    description="A lightweight, modern web-based hosting panel",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "system_monitor": "running"
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - redirect to admin panel"""
    return {
        "message": "Modern Hosting Panel API",
        "docs": "/api/docs",
        "admin": "/admin"
    }


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 