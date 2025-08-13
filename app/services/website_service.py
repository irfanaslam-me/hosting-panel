"""
Website service for managing website operations
"""

import os
import shutil
import subprocess
import asyncio
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.core.database import Website, Database, Backup
from app.schemas.website import WebsiteCreate, WebsiteUpdate, WebsiteStats
from app.services.web_server_service import WebServerService
from app.services.database_service import DatabaseService


class WebsiteService:
    """Service for managing websites"""
    
    def __init__(self, db: Session):
        self.db = db
        self.web_server_service = WebServerService()
        self.database_service = DatabaseService(db)
    
    async def create_website(self, website_data: WebsiteCreate, owner_id: int) -> Website:
        """Create a new website"""
        # Extract domain name for directory
        domain_name = website_data.domain.split('.')[0]
        document_root = website_data.document_root or f"{settings.BASE_DIR}/{domain_name}"
        
        # Create website directory
        os.makedirs(document_root, exist_ok=True)
        
        # Set proper permissions
        subprocess.run(["chown", "-R", "www-data:www-data", document_root])
        subprocess.run(["chmod", "-R", "755", document_root])
        
        # Create website record
        website = Website(
            domain=website_data.domain,
            name=website_data.name,
            type=website_data.type,
            document_root=document_root,
            php_version=website_data.php_version,
            ssl_enabled=website_data.ssl_enabled,
            owner_id=owner_id
        )
        
        self.db.add(website)
        self.db.commit()
        self.db.refresh(website)
        
        # Setup website based on type
        await self._setup_website_by_type(website, website_data.type)
        
        # Create virtual host configuration
        await self.web_server_service.create_virtual_host(website)
        
        # Reload web server
        await self.web_server_service.reload()
        
        return website
    
    async def update_website(self, website_id: int, website_data: WebsiteUpdate) -> Website:
        """Update a website"""
        website = self.db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError("Website not found")
        
        # Update fields
        if website_data.name is not None:
            website.name = website_data.name
        
        if website_data.status is not None:
            website.status = website_data.status
        
        if website_data.php_version is not None:
            website.php_version = website_data.php_version
        
        if website_data.ssl_enabled is not None:
            website.ssl_enabled = website_data.ssl_enabled
        
        website.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(website)
        
        # Update virtual host configuration
        await self.web_server_service.update_virtual_host(website)
        await self.web_server_service.reload()
        
        return website
    
    async def delete_website(self, website_id: int):
        """Delete a website"""
        website = self.db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError("Website not found")
        
        # Delete virtual host configuration
        await self.web_server_service.delete_virtual_host(website)
        
        # Delete website directory
        if os.path.exists(website.document_root):
            shutil.rmtree(website.document_root)
        
        # Delete associated databases
        databases = self.db.query(Database).filter(Database.website_id == website_id).all()
        for database in databases:
            await self.database_service.delete_database(database.id)
        
        # Delete website record
        self.db.delete(website)
        self.db.commit()
        
        # Reload web server
        await self.web_server_service.reload()
    
    async def get_website_stats(self, website_id: int) -> WebsiteStats:
        """Get website statistics"""
        website = self.db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError("Website not found")
        
        # Calculate disk usage
        disk_usage = 0
        if os.path.exists(website.document_root):
            for dirpath, dirnames, filenames in os.walk(website.document_root):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        disk_usage += os.path.getsize(filepath)
                    except OSError:
                        pass
        
        # Get last backup
        last_backup = self.db.query(Backup).filter(
            Backup.name.like(f"%{website.domain}%")
        ).order_by(Backup.created_at.desc()).first()
        
        return WebsiteStats(
            disk_usage=disk_usage,
            bandwidth_usage=0,  # TODO: Implement bandwidth tracking
            requests_per_day=0,  # TODO: Implement request tracking
            uptime_percentage=100.0,  # TODO: Implement uptime monitoring
            last_backup=last_backup.created_at if last_backup else None
        )
    
    async def create_backup(self, website_id: int) -> Backup:
        """Create a backup of the website"""
        website = self.db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError("Website not found")
        
        # Create backup filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{website.domain}_{timestamp}.tar.gz"
        backup_path = os.path.join(settings.BACKUP_PATH, backup_filename)
        
        # Create backup
        subprocess.run([
            "tar", "-czf", backup_path, "-C", settings.BASE_DIR, 
            os.path.basename(website.document_root)
        ])
        
        # Get backup size
        backup_size = os.path.getsize(backup_path)
        
        # Create backup record
        backup = Backup(
            name=backup_filename,
            type="website",
            path=backup_path,
            size=backup_size,
            status="completed"
        )
        
        self.db.add(backup)
        self.db.commit()
        self.db.refresh(backup)
        
        return backup
    
    async def restart_website(self, website_id: int):
        """Restart a website"""
        website = self.db.query(Website).filter(Website.id == website_id).first()
        if not website:
            raise ValueError("Website not found")
        
        # Reload web server configuration
        await self.web_server_service.reload()
    
    async def _setup_website_by_type(self, website: Website, website_type: str):
        """Setup website based on its type"""
        if website_type == "wordpress":
            await self._setup_wordpress(website)
        elif website_type == "php":
            await self._setup_php(website)
        elif website_type == "static":
            await self._setup_static(website)
        elif website_type == "python":
            await self._setup_python(website)
        elif website_type == "docker":
            await self._setup_docker(website)
    
    async def _setup_wordpress(self, website: Website):
        """Setup WordPress website"""
        # Download WordPress
        subprocess.run([
            "wget", "https://wordpress.org/latest.tar.gz", 
            "-O", f"{website.document_root}/wordpress.tar.gz"
        ], cwd=website.document_root)
        
        # Extract WordPress
        subprocess.run([
            "tar", "-xzf", "wordpress.tar.gz", "--strip-components=1"
        ], cwd=website.document_root)
        
        # Clean up
        os.remove(f"{website.document_root}/wordpress.tar.gz")
        
        # Set permissions
        subprocess.run(["chown", "-R", "www-data:www-data", website.document_root])
        subprocess.run(["chmod", "-R", "755", website.document_root])
    
    async def _setup_php(self, website: Website):
        """Setup PHP website"""
        # Create index.php file
        index_content = """<!DOCTYPE html>
<html>
<head>
    <title><?php echo htmlspecialchars($_SERVER['HTTP_HOST']); ?></title>
</head>
<body>
    <h1>Welcome to <?php echo htmlspecialchars($_SERVER['HTTP_HOST']); ?></h1>
    <p>PHP version: <?php echo phpversion(); ?></p>
    <p>Server time: <?php echo date('Y-m-d H:i:s'); ?></p>
</body>
</html>"""
        
        with open(f"{website.document_root}/index.php", "w") as f:
            f.write(index_content)
    
    async def _setup_static(self, website: Website):
        """Setup static website"""
        # Create index.html file
        index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Welcome to {domain}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to {domain}</h1>
        <p>Your static website is ready!</p>
        <p>Upload your files to this directory to get started.</p>
    </div>
</body>
</html>""".format(domain=website.domain)
        
        with open(f"{website.document_root}/index.html", "w") as f:
            f.write(index_content)
    
    async def _setup_python(self, website: Website):
        """Setup Python website"""
        # Create requirements.txt
        requirements_content = """Flask==2.3.3
gunicorn==21.2.0"""
        
        with open(f"{website.document_root}/requirements.txt", "w") as f:
            f.write(requirements_content)
        
        # Create app.py
        app_content = """from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Welcome to {{ domain }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to {{ domain }}</h1>
                <p>Your Python Flask application is ready!</p>
                <p>Edit app.py to customize your application.</p>
            </div>
        </body>
        </html>
    ''', domain='{domain}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)""".format(domain=website.domain)
        
        with open(f"{website.document_root}/app.py", "w") as f:
            f.write(app_content)
    
    async def _setup_docker(self, website: Website):
        """Setup Docker website"""
        # Create docker-compose.yml
        docker_compose_content = """version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    restart: unless-stopped"""
        
        with open(f"{website.document_root}/docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        
        # Create html directory and index.html
        os.makedirs(f"{website.document_root}/html", exist_ok=True)
        
        index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Welcome to {domain}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to {domain}</h1>
        <p>Your Docker container is ready!</p>
        <p>Edit the docker-compose.yml file to customize your setup.</p>
    </div>
</body>
</html>""".format(domain=website.domain)
        
        with open(f"{website.document_root}/html/index.html", "w") as f:
            f.write(index_content) 