"""
Docker service for managing containers and images
"""

import docker
import subprocess
import os
from typing import Dict, Any, List
from app.core.config import settings


class DockerService:
    """Service for managing Docker containers and images"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception:
            self.client = None
    
    async def get_containers(self) -> List[Dict[str, Any]]:
        """Get all Docker containers"""
        if not self.client:
            return {"error": "Docker client not available"}
        
        try:
            containers = self.client.containers.list(all=True)
            return [
                {
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else container.image.id,
                    "ports": container.ports,
                    "created": container.attrs["Created"],
                    "state": container.attrs["State"]
                }
                for container in containers
            ]
        except Exception as e:
            return {"error": str(e)}
    
    async def get_container(self, container_id: str) -> Dict[str, Any]:
        """Get a specific Docker container"""
        if not self.client:
            return {"error": "Docker client not available"}
        
        try:
            container = self.client.containers.get(container_id)
            return {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else container.image.id,
                "ports": container.ports,
                "created": container.attrs["Created"],
                "state": container.attrs["State"],
                "config": container.attrs["Config"],
                "network_settings": container.attrs["NetworkSettings"]
            }
        except docker.errors.NotFound:
            return {"error": "Container not found"}
        except Exception as e:
            return {"error": str(e)}
    
    async def start_container(self, container_id: str) -> Dict[str, Any]:
        """Start a Docker container"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            container = self.client.containers.get(container_id)
            container.start()
            return {"success": True, "message": "Container started successfully"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def stop_container(self, container_id: str) -> Dict[str, Any]:
        """Stop a Docker container"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            return {"success": True, "message": "Container stopped successfully"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def restart_container(self, container_id: str) -> Dict[str, Any]:
        """Restart a Docker container"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            container = self.client.containers.get(container_id)
            container.restart()
            return {"success": True, "message": "Container restarted successfully"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_container(self, container_id: str) -> Dict[str, Any]:
        """Delete a Docker container"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=True)
            return {"success": True, "message": "Container deleted successfully"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Container not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_images(self) -> List[Dict[str, Any]]:
        """Get all Docker images"""
        if not self.client:
            return {"error": "Docker client not available"}
        
        try:
            images = self.client.images.list()
            return [
                {
                    "id": image.id,
                    "tags": image.tags,
                    "size": image.attrs["Size"],
                    "created": image.attrs["Created"],
                    "architecture": image.attrs["Architecture"]
                }
                for image in images
            ]
        except Exception as e:
            return {"error": str(e)}
    
    async def compose_up(self, compose_file: str) -> Dict[str, Any]:
        """Start Docker Compose services"""
        try:
            if not os.path.exists(compose_file):
                return {"success": False, "error": "Docker Compose file not found"}
            
            result = subprocess.run([
                "docker-compose", "-f", compose_file, "up", "-d"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {"success": True, "message": "Docker Compose services started successfully"}
            else:
                return {"success": False, "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Docker Compose operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def compose_down(self, compose_file: str) -> Dict[str, Any]:
        """Stop Docker Compose services"""
        try:
            if not os.path.exists(compose_file):
                return {"success": False, "error": "Docker Compose file not found"}
            
            result = subprocess.run([
                "docker-compose", "-f", compose_file, "down"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {"success": True, "message": "Docker Compose services stopped successfully"}
            else:
                return {"success": False, "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Docker Compose operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def pull_image(self, image_name: str) -> Dict[str, Any]:
        """Pull a Docker image"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            self.client.images.pull(image_name)
            return {"success": True, "message": f"Image {image_name} pulled successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def remove_image(self, image_id: str) -> Dict[str, Any]:
        """Remove a Docker image"""
        if not self.client:
            return {"success": False, "error": "Docker client not available"}
        
        try:
            self.client.images.remove(image_id, force=True)
            return {"success": True, "message": "Image removed successfully"}
        except docker.errors.NotFound:
            return {"success": False, "error": "Image not found"}
        except Exception as e:
            return {"success": False, "error": str(e)} 