"""
Database configuration and models for the Modern Hosting Panel
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    websites = relationship("Website", back_populates="owner")


class Website(Base):
    """Website model"""
    __tablename__ = "websites"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String)  # wordpress, php, static, python, docker
    status = Column(String, default="active")  # active, inactive, suspended
    document_root = Column(String)
    php_version = Column(String, nullable=True)
    ssl_enabled = Column(Boolean, default=False)
    ssl_cert_path = Column(String, nullable=True)
    ssl_key_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="websites")
    databases = relationship("Database", back_populates="website")


class Database(Base):
    """Database model"""
    __tablename__ = "databases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)
    type = Column(String, default="mysql")  # mysql, postgresql
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    
    # Foreign keys
    website_id = Column(Integer, ForeignKey("websites.id"))
    
    # Relationships
    website = relationship("Website", back_populates="databases")


class EmailAccount(Base):
    """Email account model"""
    __tablename__ = "email_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    domain = Column(String)
    quota = Column(Integer, default=1000)  # MB
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"))


class SystemLog(Base):
    """System log model"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)  # info, warning, error
    message = Column(Text)
    source = Column(String)  # website, database, email, system
    created_at = Column(DateTime, default=func.now())


class Backup(Base):
    """Backup model"""
    __tablename__ = "backups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # website, database, full
    path = Column(String)
    size = Column(Integer)  # bytes
    status = Column(String, default="completed")  # completed, failed, in_progress
    created_at = Column(DateTime, default=func.now())


class DockerContainer(Base):
    """Docker container model"""
    __tablename__ = "docker_containers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    image = Column(String)
    status = Column(String, default="stopped")  # running, stopped, paused
    ports = Column(Text)  # JSON string of port mappings
    volumes = Column(Text)  # JSON string of volume mappings
    environment = Column(Text)  # JSON string of environment variables
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create backup directory if it doesn't exist
    os.makedirs(settings.BACKUP_PATH, exist_ok=True)
    
    # Create base directory if it doesn't exist
    os.makedirs(settings.BASE_DIR, exist_ok=True) 