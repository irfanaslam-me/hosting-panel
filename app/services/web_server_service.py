"""
Web server service for managing Nginx and Apache configurations
"""

import os
import subprocess
from typing import Optional
from app.core.config import settings
from app.core.database import Website


class WebServerService:
    """Service for managing web server configurations"""
    
    def __init__(self):
        self.web_server = settings.WEB_SERVER
        self.conf_dir = getattr(settings, f"{self.web_server.upper()}_CONF_DIR")
        self.enabled_dir = getattr(settings, f"{self.web_server.upper()}_ENABLED_DIR")
    
    async def create_virtual_host(self, website: Website):
        """Create virtual host configuration for a website"""
        if self.web_server == "nginx":
            await self._create_nginx_vhost(website)
        elif self.web_server == "apache":
            await self._create_apache_vhost(website)
    
    async def update_virtual_host(self, website: Website):
        """Update virtual host configuration for a website"""
        if self.web_server == "nginx":
            await self._update_nginx_vhost(website)
        elif self.web_server == "apache":
            await self._update_apache_vhost(website)
    
    async def delete_virtual_host(self, website: Website):
        """Delete virtual host configuration for a website"""
        domain_name = website.domain.split('.')[0]
        config_file = f"{self.conf_dir}/{domain_name}.conf"
        enabled_file = f"{self.enabled_dir}/{domain_name}.conf"
        
        # Remove configuration files
        if os.path.exists(config_file):
            os.remove(config_file)
        
        if os.path.exists(enabled_file):
            os.remove(enabled_file)
    
    async def reload(self):
        """Reload web server configuration"""
        if self.web_server == "nginx":
            subprocess.run(["systemctl", "reload", "nginx"])
        elif self.web_server == "apache":
            subprocess.run(["systemctl", "reload", "apache2"])
    
    async def _create_nginx_vhost(self, website: Website):
        """Create Nginx virtual host configuration"""
        domain_name = website.domain.split('.')[0]
        config_file = f"{self.conf_dir}/{domain_name}.conf"
        
        # Create Nginx configuration
        config_content = f"""server {{
    listen 80;
    server_name {website.domain} www.{website.domain};
    root {website.document_root};
    index index.php index.html index.htm;

    # Logs
    access_log /var/log/nginx/{domain_name}.access.log;
    error_log /var/log/nginx/{domain_name}.error.log;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Handle PHP files
    location ~ \.php$ {{
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php/php{website.php_version or '8.1'}-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }}

    # Handle static files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|txt)$ {{
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    # Main location block
    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    # Deny access to hidden files
    location ~ /\. {{
        deny all;
    }}
}}"""
        
        # Write configuration file
        with open(config_file, "w") as f:
            f.write(config_content)
        
        # Enable site
        subprocess.run(["ln", "-sf", config_file, f"{self.enabled_dir}/{domain_name}.conf"])
    
    async def _create_apache_vhost(self, website: Website):
        """Create Apache virtual host configuration"""
        domain_name = website.domain.split('.')[0]
        config_file = f"{self.conf_dir}/{domain_name}.conf"
        
        # Create Apache configuration
        config_content = f"""<VirtualHost *:80>
    ServerName {website.domain}
    ServerAlias www.{website.domain}
    DocumentRoot {website.document_root}
    
    <Directory "{website.document_root}">
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${{APACHE_LOG_DIR}}/{domain_name}.error.log
    CustomLog ${{APACHE_LOG_DIR}}/{domain_name}.access.log combined
</VirtualHost>"""
        
        # Write configuration file
        with open(config_file, "w") as f:
            f.write(config_content)
        
        # Enable site
        subprocess.run(["a2ensite", f"{domain_name}.conf"])
    
    async def _update_nginx_vhost(self, website: Website):
        """Update Nginx virtual host configuration"""
        await self._create_nginx_vhost(website)
    
    async def _update_apache_vhost(self, website: Website):
        """Update Apache virtual host configuration"""
        await self._create_apache_vhost(website)
    
    async def install_ssl(self, domain: str, cert_path: str, key_path: str):
        """Install SSL certificate for a domain"""
        domain_name = domain.split('.')[0]
        
        if self.web_server == "nginx":
            await self._install_nginx_ssl(domain_name, domain, cert_path, key_path)
        elif self.web_server == "apache":
            await self._install_apache_ssl(domain_name, domain, cert_path, key_path)
    
    async def _install_nginx_ssl(self, domain_name: str, domain: str, cert_path: str, key_path: str):
        """Install SSL certificate for Nginx"""
        config_file = f"{self.conf_dir}/{domain_name}.conf"
        
        # Update configuration with SSL
        ssl_config = f"""
# Redirect HTTP to HTTPS
server {{
    listen 80;
    server_name {domain} www.{domain};
    return 301 https://$server_name$request_uri;
}}

# HTTPS server
server {{
    listen 443 ssl http2;
    server_name {domain} www.{domain};
    root {settings.BASE_DIR}/{domain_name};
    index index.php index.html index.htm;

    # SSL configuration
    ssl_certificate {cert_path};
    ssl_certificate_key {key_path};
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Logs
    access_log /var/log/nginx/{domain_name}.access.log;
    error_log /var/log/nginx/{domain_name}.error.log;

    # Handle PHP files
    location ~ \.php$ {{
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }}

    # Handle static files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|txt)$ {{
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    # Main location block
    location / {{
        try_files $uri $uri/ /index.php?$args;
    }}

    # Deny access to hidden files
    location ~ /\. {{
        deny all;
    }}
}}"""
        
        # Write updated configuration
        with open(config_file, "w") as f:
            f.write(ssl_config)
    
    async def _install_apache_ssl(self, domain_name: str, domain: str, cert_path: str, key_path: str):
        """Install SSL certificate for Apache"""
        config_file = f"{self.conf_dir}/{domain_name}.conf"
        
        # Update configuration with SSL
        ssl_config = f"""# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName {domain}
    ServerAlias www.{domain}
    Redirect permanent / https://{domain}/
</VirtualHost>

# HTTPS server
<VirtualHost *:443>
    ServerName {domain}
    ServerAlias www.{domain}
    DocumentRoot {settings.BASE_DIR}/{domain_name}
    
    SSLEngine on
    SSLCertificateFile {cert_path}
    SSLCertificateKeyFile {key_path}
    
    <Directory "{settings.BASE_DIR}/{domain_name}">
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${{APACHE_LOG_DIR}}/{domain_name}.error.log
    CustomLog ${{APACHE_LOG_DIR}}/{domain_name}.access.log combined
</VirtualHost>"""
        
        # Write updated configuration
        with open(config_file, "w") as f:
            f.write(ssl_config) 