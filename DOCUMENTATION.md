# Modern Hosting Panel Documentation

## Overview

The Modern Hosting Panel is a lightweight, feature-rich web-based hosting management system built with Python FastAPI and Vue.js. It provides a modern interface for managing websites, databases, email accounts, Docker containers, and system resources.

## Features

### Core Features
- **Website Management**: Create and manage WordPress, PHP, static, Python, and Docker websites
- **Database Management**: MySQL/MariaDB database creation and management
- **SSL Certificate Management**: Automatic SSL with Let's Encrypt integration
- **Email Server**: Optional Postfix/Dovecot email server setup
- **Docker Support**: Container and image management with docker-compose support
- **System Monitoring**: Real-time system resource monitoring
- **Backup Management**: Automated backup creation and management
- **User Management**: Role-based access control with admin and regular users

### Supported Website Types
1. **WordPress**: Automatic WordPress installation with database setup
2. **PHP Applications**: PHP 7.4, 8.0, 8.1, 8.2 support
3. **Static Websites**: Simple HTML/CSS/JS websites
4. **Python Applications**: Flask/FastAPI applications with requirements.txt
5. **Docker Containers**: Docker and docker-compose support

## Architecture

### Backend (Python FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy ORM with MySQL/SQLite support
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **API**: RESTful API with automatic OpenAPI documentation
- **Services**: Modular service architecture for different functionalities

### Frontend (Vue.js)
- **Framework**: Vue.js 3 with Composition API
- **Styling**: Tailwind CSS for modern, responsive design
- **HTTP Client**: Axios for API communication
- **Icons**: Font Awesome for consistent iconography

### System Integration
- **Web Server**: Nginx (recommended) or Apache support
- **Database**: MySQL/MariaDB for data persistence
- **Process Manager**: Systemd for service management
- **Monitoring**: psutil for system resource tracking

## Installation

### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Python 3.8+
- MySQL/MariaDB
- Nginx or Apache
- Docker (optional)

### Quick Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hosting-panel
   ```

2. **Run the installation script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Access the panel**:
   - URL: `http://your-server-ip`
   - Username: `admin`
   - Password: `admin123`

### Manual Installation

1. **Install system dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip python3-venv nginx mysql-server
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure database**:
   ```bash
   sudo mysql -e "CREATE DATABASE hosting_panel;"
   sudo mysql -e "CREATE USER 'hosting_panel'@'localhost' IDENTIFIED BY 'password';"
   sudo mysql -e "GRANT ALL PRIVILEGES ON hosting_panel.* TO 'hosting_panel'@'localhost';"
   ```

4. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Application settings
SECRET_KEY=your-secret-key-here
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=mysql://hosting_panel:password@localhost/hosting_panel

# Web server
WEB_SERVER=nginx
PHP_VERSIONS=7.4,8.0,8.1,8.2
DEFAULT_PHP_VERSION=8.1

# SSL
CERTBOT_EMAIL=admin@yourdomain.com
SSL_PROVIDER=letsencrypt

# Admin user
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=secure-password

# Optional services
EMAIL_ENABLED=false
DNS_ENABLED=false
DOCKER_ENABLED=true
BACKUP_ENABLED=true
```

### Web Server Configuration

#### Nginx Configuration
The installation script automatically configures Nginx. For manual configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/hosting-panel/app/static/;
    }
}
```

#### Apache Configuration
For Apache users, enable the proxy modules:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```

## API Documentation

### Authentication

All API endpoints require authentication except `/auth/login`.

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=password
```

#### Using the API
Include the JWT token in the Authorization header:
```http
Authorization: Bearer <your-jwt-token>
```

### Main Endpoints

#### Websites
- `GET /api/v1/websites/` - List websites
- `POST /api/v1/websites/` - Create website
- `GET /api/v1/websites/{id}` - Get website details
- `PUT /api/v1/websites/{id}` - Update website
- `DELETE /api/v1/websites/{id}` - Delete website
- `POST /api/v1/websites/{id}/ssl` - Install SSL certificate
- `POST /api/v1/websites/{id}/backup` - Create backup

#### Databases
- `GET /api/v1/databases/` - List databases
- `POST /api/v1/databases/` - Create database
- `GET /api/v1/databases/{id}` - Get database details
- `PUT /api/v1/databases/{id}` - Update database
- `DELETE /api/v1/databases/{id}` - Delete database

#### System
- `GET /api/v1/system/status` - System status
- `GET /api/v1/system/resources` - Resource usage
- `GET /api/v1/system/services` - Service status
- `POST /api/v1/system/backup` - Create system backup

#### Docker
- `GET /api/v1/docker/containers` - List containers
- `POST /api/v1/docker/containers/{id}/start` - Start container
- `POST /api/v1/docker/containers/{id}/stop` - Stop container
- `DELETE /api/v1/docker/containers/{id}` - Delete container

## Usage Guide

### Creating a Website

1. **Login to the panel**
2. **Click "Add Website"**
3. **Fill in the details**:
   - Domain: `example.com`
   - Name: `My Website`
   - Type: Choose from WordPress, PHP, Static, Python, or Docker
4. **Click "Create"**

The system will:
- Create the website directory
- Set up the appropriate files based on type
- Configure the web server virtual host
- Reload the web server

### Installing SSL Certificate

1. **Navigate to your website**
2. **Click "Install SSL"**
3. **Enter your email address**
4. **Click "Install"**

The system will:
- Install Certbot if not present
- Obtain SSL certificate from Let's Encrypt
- Configure the web server for HTTPS
- Set up automatic renewal

### Managing Databases

1. **Go to "Databases" section**
2. **Click "Add Database"**
3. **Enter database details**:
   - Name: `myapp_db`
   - Username: `myapp_user`
   - Password: `secure_password`
4. **Click "Create"**

### Docker Management

1. **Go to "Docker" section**
2. **View running containers**
3. **Use actions to start/stop/restart containers**
4. **Upload docker-compose.yml files for multi-container applications**

## Security Considerations

### Production Deployment

1. **Change default passwords**:
   - Admin password
   - Database passwords
   - SSL certificate passwords

2. **Configure firewall**:
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

3. **Set up SSL certificates**:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

4. **Regular updates**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

5. **Backup strategy**:
   - Configure automated backups
   - Store backups off-site
   - Test backup restoration

### Security Best Practices

1. **Use strong passwords**
2. **Enable two-factor authentication** (if available)
3. **Regular security updates**
4. **Monitor system logs**
5. **Limit access to admin panel**
6. **Use HTTPS everywhere**
7. **Regular backup testing**

## Troubleshooting

### Common Issues

#### Service Not Starting
```bash
# Check service status
sudo systemctl status hosting-panel

# View logs
sudo journalctl -u hosting-panel -f

# Check configuration
python main.py --check-config
```

#### Database Connection Issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u hosting_panel -p hosting_panel

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log
```

#### Web Server Issues
```bash
# Check Nginx status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

#### SSL Certificate Issues
```bash
# Check Certbot status
sudo certbot certificates

# Renew certificates
sudo certbot renew

# Check SSL configuration
openssl s_client -connect your-domain.com:443
```

### Log Files

- **Application logs**: `/var/log/hosting-panel/`
- **Nginx logs**: `/var/log/nginx/`
- **MySQL logs**: `/var/log/mysql/`
- **System logs**: `/var/log/syslog`

### Performance Optimization

1. **Enable caching**:
   - Redis for session storage
   - Nginx caching for static files
   - Database query optimization

2. **Resource monitoring**:
   - Monitor CPU and memory usage
   - Set up alerts for high resource usage
   - Regular performance reviews

3. **Database optimization**:
   - Regular database maintenance
   - Query optimization
   - Proper indexing

## Development

### Project Structure
```
hosting-panel/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic
│   └── static/        # Frontend files
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
├── install.sh         # Installation script
└── README.md          # Project documentation
```

### Adding New Features

1. **Create service class** in `app/services/`
2. **Define schemas** in `app/schemas/`
3. **Create API endpoints** in `app/api/v1/endpoints/`
4. **Update frontend** in `app/static/`
5. **Add tests** (recommended)

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

### Getting Help

1. **Check the documentation**
2. **Search existing issues**
3. **Create a new issue** with:
   - Detailed description
   - Steps to reproduce
   - System information
   - Log files

### Community

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For general questions and community support
- **Wiki**: For additional documentation and guides

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Vue.js for the frontend framework
- Tailwind CSS for the styling framework
- All contributors and community members 