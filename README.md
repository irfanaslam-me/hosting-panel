# Modern Hosting Panel

A lightweight, modern web-based hosting panel for managing WordPress, PHP, static websites, Python applications, and Docker containers.

## Features

### Core Functionality
- **Web Server Management**: Support for both Nginx and Apache
- **Website Management**: Create, edit, and delete websites
- **Database Management**: MySQL/MariaDB database creation and management
- **SSL Certificate Management**: Automatic SSL with Let's Encrypt
- **Email Server**: Optional Postfix/Dovecot integration
- **DNS Management**: Optional DNS server integration
- **Docker Support**: Container management with docker-compose
- **Backup Management**: Automated backups for websites and databases

### Supported Website Types
- WordPress (automatic installation)
- PHP applications
- Static websites
- Python web applications
- Docker containers

### Modern Features
- Real-time system monitoring
- Resource usage tracking
- Modern responsive UI
- API-first architecture
- Plugin system for extensibility
- Multi-user support with role-based access

## Architecture

- **Backend**: Python FastAPI
- **Frontend**: React with TypeScript
- **Database**: SQLite (lightweight) or PostgreSQL (production)
- **Web Server**: Nginx (recommended) or Apache
- **Process Manager**: Systemd integration

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `python main.py`
4. Access the panel at `http://localhost:8000`

## Configuration

The panel supports both simple and advanced configurations:
- **Simple Mode**: Basic hosting with minimal resource usage
- **Advanced Mode**: Full feature set with optional services

## Security Features

- Role-based access control
- API authentication
- SSL/TLS encryption
- Firewall management
- Regular security updates

## License

MIT License 