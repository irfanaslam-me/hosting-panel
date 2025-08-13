"""
Database service for managing MySQL/MariaDB databases
"""

import subprocess
import os
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.core.database import Database, Backup
from app.schemas.database import DatabaseCreate, DatabaseUpdate


class DatabaseService:
    """Service for managing databases"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_database(self, database_data: DatabaseCreate) -> Database:
        """Create a new database"""
        # Create database using MySQL command
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", f"CREATE DATABASE {database_data.name};"
        ], input=b"root_password\n", check=True)
        
        # Create database user
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", 
            f"CREATE USER '{database_data.username}'@'localhost' IDENTIFIED BY '{database_data.password}';"
        ], input=b"root_password\n", check=True)
        
        # Grant privileges
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", 
            f"GRANT ALL PRIVILEGES ON {database_data.name}.* TO '{database_data.username}'@'localhost';"
        ], input=b"root_password\n", check=True)
        
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", "FLUSH PRIVILEGES;"
        ], input=b"root_password\n", check=True)
        
        # Create database record
        database = Database(
            name=database_data.name,
            username=database_data.username,
            password=database_data.password,
            type=database_data.type
        )
        
        self.db.add(database)
        self.db.commit()
        self.db.refresh(database)
        
        return database
    
    async def update_database(self, database_id: int, database_data: DatabaseUpdate) -> Database:
        """Update a database"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Update password if provided
        if database_data.password is not None:
            subprocess.run([
                "mysql", "-u", "root", "-p", "-e", 
                f"ALTER USER '{database.username}'@'localhost' IDENTIFIED BY '{database_data.password}';"
            ], input=b"root_password\n", check=True)
            
            database.password = database_data.password
        
        # Update status if provided
        if database_data.status is not None:
            database.status = database_data.status
        
        self.db.commit()
        self.db.refresh(database)
        
        return database
    
    async def delete_database(self, database_id: int):
        """Delete a database"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Drop database
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", f"DROP DATABASE {database.name};"
        ], input=b"root_password\n", check=True)
        
        # Drop user
        subprocess.run([
            "mysql", "-u", "root", "-p", "-e", f"DROP USER '{database.username}'@'localhost';"
        ], input=b"root_password\n", check=True)
        
        # Delete database record
        self.db.delete(database)
        self.db.commit()
    
    async def create_backup(self, database_id: int) -> Backup:
        """Create a backup of the database"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Create backup filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{database.name}_{timestamp}.sql"
        backup_path = os.path.join(settings.BACKUP_PATH, backup_filename)
        
        # Create backup using mysqldump
        subprocess.run([
            "mysqldump", "-u", database.username, f"-p{database.password}", 
            database.name, "--result-file", backup_path
        ], check=True)
        
        # Get backup size
        backup_size = os.path.getsize(backup_path)
        
        # Create backup record
        backup = Backup(
            name=backup_filename,
            type="database",
            path=backup_path,
            size=backup_size,
            status="completed"
        )
        
        self.db.add(backup)
        self.db.commit()
        self.db.refresh(backup)
        
        return backup
    
    async def restore_backup(self, database_id: int, backup_path: str):
        """Restore a database from backup"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Restore database from backup
        subprocess.run([
            "mysql", "-u", database.username, f"-p{database.password}", 
            database.name, "<", backup_path
        ], shell=True, check=True)
    
    async def get_database_stats(self, database_id: int) -> dict:
        """Get database statistics"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Get database size
        result = subprocess.run([
            "mysql", "-u", database.username, f"-p{database.password}", "-e",
            f"SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS 'DB Size in MB' FROM information_schema.tables WHERE table_schema = '{database.name}';"
        ], capture_output=True, text=True, check=True)
        
        # Parse size from output
        size_line = result.stdout.strip().split('\n')[-1]
        size_mb = float(size_line) if size_line.replace('.', '').isdigit() else 0
        
        # Get table count
        result = subprocess.run([
            "mysql", "-u", database.username, f"-p{database.password}", "-e",
            f"SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = '{database.name}';"
        ], capture_output=True, text=True, check=True)
        
        table_count_line = result.stdout.strip().split('\n')[-1]
        table_count = int(table_count_line) if table_count_line.isdigit() else 0
        
        return {
            "size_mb": size_mb,
            "table_count": table_count,
            "connections": 0,  # TODO: Implement connection tracking
            "queries_per_second": 0  # TODO: Implement query tracking
        }
    
    async def optimize_database(self, database_id: int):
        """Optimize database tables"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Get all tables
        result = subprocess.run([
            "mysql", "-u", database.username, f"-p{database.password}", "-e",
            f"SHOW TABLES FROM {database.name};"
        ], capture_output=True, text=True, check=True)
        
        tables = result.stdout.strip().split('\n')[1:]  # Skip header
        
        # Optimize each table
        for table in tables:
            if table.strip():
                subprocess.run([
                    "mysql", "-u", database.username, f"-p{database.password}", "-e",
                    f"OPTIMIZE TABLE {database.name}.{table.strip()};"
                ], check=True)
    
    async def repair_database(self, database_id: int):
        """Repair database tables"""
        database = self.db.query(Database).filter(Database.id == database_id).first()
        if not database:
            raise ValueError("Database not found")
        
        # Get all tables
        result = subprocess.run([
            "mysql", "-u", database.username, f"-p{database.password}", "-e",
            f"SHOW TABLES FROM {database.name};"
        ], capture_output=True, text=True, check=True)
        
        tables = result.stdout.strip().split('\n')[1:]  # Skip header
        
        # Repair each table
        for table in tables:
            if table.strip():
                subprocess.run([
                    "mysql", "-u", database.username, f"-p{database.password}", "-e",
                    f"REPAIR TABLE {database.name}.{table.strip()};"
                ], check=True) 