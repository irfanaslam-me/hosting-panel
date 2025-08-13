"""
SSL service for managing SSL certificates
"""

import subprocess
import os
from typing import Dict, Any
from app.core.config import settings


class SSLService:
    """Service for managing SSL certificates"""
    
    def __init__(self, db=None):
        self.db = db
    
    async def install_ssl(self, domain: str) -> Dict[str, Any]:
        """Install SSL certificate using Let's Encrypt"""
        try:
            # Check if certbot is installed
            if not self._is_certbot_installed():
                await self._install_certbot()
            
            # Install SSL certificate
            result = subprocess.run([
                "certbot", "certonly", "--webroot",
                "--webroot-path", f"{settings.BASE_DIR}/{domain.split('.')[0]}",
                "--email", settings.CERTBOT_EMAIL or "admin@localhost",
                "--agree-tos", "--no-eff-email",
                "--domains", domain, f"www.{domain}",
                "--non-interactive"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Certificate installed successfully
                cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
                key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"
                
                # Update web server configuration
                web_server_service = WebServerService()
                await web_server_service.install_ssl(domain, cert_path, key_path)
                await web_server_service.reload()
                
                return {
                    "success": True,
                    "message": "SSL certificate installed successfully",
                    "cert_path": cert_path,
                    "key_path": key_path
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to install SSL certificate: {result.stderr}",
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error installing SSL certificate: {str(e)}",
                "error": str(e)
            }
    
    async def renew_ssl(self, domain: str) -> Dict[str, Any]:
        """Renew SSL certificate"""
        try:
            result = subprocess.run([
                "certbot", "renew", "--cert-name", domain,
                "--non-interactive"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Reload web server after renewal
                web_server_service = WebServerService()
                await web_server_service.reload()
                
                return {
                    "success": True,
                    "message": "SSL certificate renewed successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to renew SSL certificate: {result.stderr}",
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error renewing SSL certificate: {str(e)}",
                "error": str(e)
            }
    
    async def revoke_ssl(self, domain: str) -> Dict[str, Any]:
        """Revoke SSL certificate"""
        try:
            result = subprocess.run([
                "certbot", "revoke", "--cert-path", f"/etc/letsencrypt/live/{domain}/cert.pem",
                "--non-interactive"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "SSL certificate revoked successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to revoke SSL certificate: {result.stderr}",
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error revoking SSL certificate: {str(e)}",
                "error": str(e)
            }
    
    def _is_certbot_installed(self) -> bool:
        """Check if certbot is installed"""
        try:
            result = subprocess.run(["certbot", "--version"], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    async def _install_certbot(self):
        """Install certbot"""
        try:
            # Update package list
            subprocess.run(["apt-get", "update"], check=True)
            
            # Install certbot
            if settings.WEB_SERVER == "nginx":
                subprocess.run([
                    "apt-get", "install", "-y", "certbot", "python3-certbot-nginx"
                ], check=True)
            elif settings.WEB_SERVER == "apache":
                subprocess.run([
                    "apt-get", "install", "-y", "certbot", "python3-certbot-apache"
                ], check=True)
            else:
                subprocess.run([
                    "apt-get", "install", "-y", "certbot"
                ], check=True)
        
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install certbot: {e}")
    
    async def get_certificate_info(self, domain: str) -> Dict[str, Any]:
        """Get SSL certificate information"""
        try:
            cert_path = f"/etc/letsencrypt/live/{domain}/cert.pem"
            
            if not os.path.exists(cert_path):
                return {
                    "success": False,
                    "message": "Certificate not found"
                }
            
            # Get certificate details
            result = subprocess.run([
                "openssl", "x509", "-in", cert_path, "-text", "-noout"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "certificate_info": result.stdout,
                    "cert_path": cert_path
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to read certificate information",
                    "error": result.stderr
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting certificate information: {str(e)}",
                "error": str(e)
            }
    
    async def setup_auto_renewal(self):
        """Setup automatic SSL certificate renewal"""
        try:
            # Create renewal script
            renewal_script = """#!/bin/bash
# Auto-renewal script for SSL certificates

# Renew certificates
certbot renew --quiet

# Reload web server
systemctl reload {web_server}
""".format(web_server=settings.WEB_SERVER)
            
            script_path = "/usr/local/bin/ssl-renew.sh"
            with open(script_path, "w") as f:
                f.write(renewal_script)
            
            # Make script executable
            os.chmod(script_path, 0o755)
            
            # Add to crontab (run twice daily)
            cron_job = f"0 0,12 * * * {script_path}"
            
            # Add to current user's crontab
            subprocess.run(["crontab", "-l"], capture_output=True)
            subprocess.run(["echo", cron_job, "|", "crontab", "-"], shell=True)
            
            return {
                "success": True,
                "message": "Auto-renewal setup completed"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error setting up auto-renewal: {str(e)}",
                "error": str(e)
            }


# Import at the end to avoid circular imports
from app.services.web_server_service import WebServerService 