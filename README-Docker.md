# Modern Hosting Panel - Docker Deployment

This guide will help you deploy the Modern Hosting Panel using Docker and Docker Compose.

## 🐳 Prerequisites

- Docker Desktop installed and running
- Docker Compose installed
- At least 4GB of available RAM
- At least 10GB of available disk space

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)

#### For Linux/macOS:
```bash
chmod +x docker-start.sh
./docker-start.sh
```

#### For Windows:
```cmd
docker-start.bat
```

### Option 2: Manual Docker Compose

```bash
# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🌐 Access Points

Once all services are running:

- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 🔑 Default Credentials

- **Username**: admin
- **Password**: admin123
- **Email**: admin@localhost

⚠️ **Important**: Change these credentials immediately after first login!

## 🏗️ Architecture

The Docker setup includes:

- **hosting_panel**: Main FastAPI application
- **postgres**: PostgreSQL 15 database
- **redis**: Redis 7 for caching and background tasks
- **nginx**: Reverse proxy (optional, for production)

## 📁 Volumes

The following data is persisted:

- `postgres_data`: Database files
- `redis_data`: Redis data and AOF files
- `website_data`: Website files and configurations
- `backup_data`: Backup files
- `log_data`: Application logs

## ⚙️ Configuration

### Environment Variables

Key environment variables can be modified in `docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql://hosting_user:hosting_password_123@postgres:5432/hosting_panel
  REDIS_URL: redis://:redis_password_123@redis:6379
  SECRET_KEY: your-super-secret-key-change-this-in-production
  ADMIN_PASSWORD: admin123
```

### Database Configuration

- **Database**: hosting_panel
- **Username**: hosting_user
- **Password**: hosting_password_123
- **Port**: 5432

### Redis Configuration

- **Port**: 6379
- **Password**: redis_password_123
- **Persistence**: Enabled (AOF)

## 🔧 Management Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Restart services
```bash
docker-compose restart
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f hosting_panel
```

### Check status
```bash
docker-compose ps
```

### Update and rebuild
```bash
docker-compose down
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   
   # Stop conflicting service or change port in docker-compose.yml
   ```

2. **Permission denied on Docker socket**
   ```bash
   # Add user to docker group (Linux)
   sudo usermod -aG docker $USER
   # Logout and login again
   ```

3. **Database connection failed**
   ```bash
   # Check if PostgreSQL is running
   docker-compose logs postgres
   
   # Restart the service
   docker-compose restart postgres
   ```

4. **Out of memory**
   - Increase Docker Desktop memory limit
   - Reduce Redis memory usage in docker-compose.yml

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs hosting_panel

# Check container status
docker-compose ps
```

## 🔒 Security Considerations

1. **Change default passwords** immediately after deployment
2. **Update SECRET_KEY** in production
3. **Restrict network access** in production environments
4. **Use secrets management** for sensitive data
5. **Enable SSL/TLS** for production use

## 📊 Monitoring

### Health Checks

All services include health checks:

- **Application**: HTTP endpoint `/health`
- **PostgreSQL**: `pg_isready` command
- **Redis**: Redis ping command

### Resource Usage

Monitor resource usage:

```bash
# View resource usage
docker stats

# View detailed container info
docker inspect hosting_panel_app
```

## 🚀 Production Deployment

For production use:

1. **Enable nginx service**:
   ```bash
   docker-compose --profile production up -d
   ```

2. **Configure SSL certificates**
3. **Set up proper firewall rules**
4. **Configure backup strategies**
5. **Set up monitoring and alerting**

## 📝 Environment File

Create a `.env` file for custom configuration:

```env
# Database
POSTGRES_PASSWORD=your_secure_password
POSTGRES_USER=your_user

# Redis
REDIS_PASSWORD=your_redis_password

# Application
SECRET_KEY=your_super_secret_key
ADMIN_PASSWORD=your_admin_password

# SSL
CERTBOT_EMAIL=your_email@domain.com
```

## 🤝 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify Docker and Docker Compose versions
3. Check system resources
4. Review the troubleshooting section above

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
