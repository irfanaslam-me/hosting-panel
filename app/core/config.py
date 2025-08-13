"""
Configuration settings for the Modern Hosting Panel
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    APP_NAME: str = "Modern Hosting Panel"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./hosting_panel.db"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            # Handle string input like "['*']" or "*" or "host1,host2"
            if v.startswith('[') and v.endswith(']'):
                # Parse list-like string "['*']" -> ["*"]
                import ast
                try:
                    return ast.literal_eval(v)
                except:
                    pass
            elif ',' in v:
                # Parse comma-separated string "host1,host2" -> ["host1", "host2"]
                return [host.strip() for host in v.split(',')]
            else:
                # Single host string "*" -> ["*"]
                return [v]
        return v
    
    # File paths
    BASE_DIR: str = "/var/www"
    NGINX_CONF_DIR: str = "/etc/nginx/sites-available"
    NGINX_ENABLED_DIR: str = "/etc/nginx/sites-enabled"
    APACHE_CONF_DIR: str = "/etc/apache2/sites-available"
    APACHE_ENABLED_DIR: str = "/etc/apache2/sites-enabled"
    
    # Web server settings
    WEB_SERVER: str = "nginx"  # nginx or apache
    PHP_VERSIONS: List[str] = ["7.4", "8.0", "8.1", "8.2"]
    DEFAULT_PHP_VERSION: str = "8.1"
    
    @validator("PHP_VERSIONS", pre=True)
    def parse_php_versions(cls, v):
        if isinstance(v, str):
            # Handle string input like "7.4,8.0,8.1,8.2"
            if ',' in v:
                return [version.strip() for version in v.split(',')]
            else:
                return [v]
        return v
    
    # SSL settings
    CERTBOT_EMAIL: Optional[str] = None
    SSL_PROVIDER: str = "letsencrypt"  # letsencrypt or custom
    
    # Email settings
    EMAIL_ENABLED: bool = False
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # DNS settings
    DNS_ENABLED: bool = False
    DNS_SERVER: str = "bind9"
    
    # Docker settings
    DOCKER_ENABLED: bool = True
    DOCKER_SOCKET: str = "/var/run/docker.sock"
    
    # Backup settings
    BACKUP_ENABLED: bool = True
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_PATH: str = "/var/backups/hosting-panel"
    
    # Monitoring
    MONITORING_ENABLED: bool = True
    MONITORING_INTERVAL: int = 60  # seconds
    
    # Admin user
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@localhost"
    ADMIN_PASSWORD: str = "admin123"  # Change this in production
    
    # Redis (for caching and background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-this-in-production":
            print("⚠️  Warning: Using default secret key. Change this in production!")
        return v
    
    @validator("ADMIN_PASSWORD")
    def validate_admin_password(cls, v):
        if v == "admin123":
            print("⚠️  Warning: Using default admin password. Change this in production!")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings() 