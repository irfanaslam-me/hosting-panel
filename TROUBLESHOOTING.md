# Docker Troubleshooting Guide

## 🚨 Common Docker Errors and Solutions

### 1. Docker Compose Version Issues

**Error**: `version '3.8' is not supported`

**Solution**: 
- Update Docker Compose to version 2.0+
- Or use the simplified compose file: `docker-compose.simple.yml`

```bash
# Check Docker Compose version
docker-compose --version

# If using old version, try:
docker compose up -d --build
```

### 2. Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```bash
# Check what's using the port
netstat -ano | findstr :8000

# Stop the conflicting service or change port in docker-compose.yml
# Change "8000:8000" to "8001:8000" for example
```

### 3. Permission Denied on Docker Socket

**Error**: `Got permission denied while trying to connect to the Docker daemon socket`

**Solution**:
```bash
# Windows: Run PowerShell as Administrator
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

### 4. Database Connection Failed

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check if PostgreSQL container is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart the service
docker-compose restart postgres
```

### 5. Redis Connection Failed

**Error**: `Connection refused` or `Authentication failed`

**Solution**:
```bash
# Check Redis container status
docker-compose ps redis

# Check Redis logs
docker-compose logs redis

# Test Redis connection
docker exec -it hosting_panel_redis redis-cli -a redis_password_123 ping
```

### 6. Build Failures

**Error**: `failed to build: error building at step`

**Solution**:
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -t test-image .
```

## 🔧 Step-by-Step Troubleshooting

### Step 1: Verify Docker Installation
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Verify Docker is running
docker info
```

### Step 2: Test Basic Docker Commands
```bash
# Test Docker with a simple container
docker run hello-world

# Test Docker Compose
docker-compose --help
```

### Step 3: Check System Resources
```bash
# Check available disk space
df -h

# Check available memory
free -h

# Check CPU usage
top
```

### Step 4: Use Simplified Compose File
If the main compose file fails, try the simplified version:

```bash
# Use simplified compose file
docker-compose -f docker-compose.simple.yml up -d --build
```

### Step 5: Check Container Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs hosting_panel
docker-compose logs postgres
docker-compose logs redis

# Follow logs in real-time
docker-compose logs -f
```

## 🐛 Specific Error Solutions

### Error: "No such file or directory"
**Cause**: Missing files or incorrect paths
**Solution**: Ensure all required files exist in the project directory

### Error: "Invalid reference format"
**Cause**: Docker image name format issue
**Solution**: Check image names in docker-compose.yml

### Error: "Network not found"
**Cause**: Docker network configuration issue
**Solution**: Remove and recreate networks:
```bash
docker-compose down
docker network prune
docker-compose up -d
```

### Error: "Volume not found"
**Cause**: Docker volume configuration issue
**Solution**: Remove and recreate volumes:
```bash
docker-compose down -v
docker volume prune
docker-compose up -d
```

## 🚀 Alternative Startup Methods

### Method 1: Start Services One by One
```bash
# Start database first
docker-compose up -d postgres

# Wait for database to be ready
sleep 10

# Start Redis
docker-compose up -d redis

# Wait for Redis to be ready
sleep 5

# Start main application
docker-compose up -d hosting_panel
```

### Method 2: Use Docker Commands Directly
```bash
# Create network
docker network create hosting_network

# Start PostgreSQL
docker run -d --name hosting_panel_postgres \
  --network hosting_network \
  -e POSTGRES_DB=hosting_panel \
  -e POSTGRES_USER=hosting_user \
  -e POSTGRES_PASSWORD=hosting_password_123 \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d --name hosting_panel_redis \
  --network hosting_network \
  -p 6379:6379 \
  redis:7-alpine redis-server --appendonly yes --requirepass redis_password_123

# Build and start application
docker build -t hosting_panel .
docker run -d --name hosting_panel_app \
  --network hosting_network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://hosting_user:hosting_password_123@hosting_panel_postgres:5432/hosting_panel \
  -e REDIS_URL=redis://:redis_password_123@hosting_panel_redis:6379 \
  hosting_panel
```

## 📋 Pre-Flight Checklist

Before running Docker Compose, ensure:

- [ ] Docker Desktop is running
- [ ] Docker Compose is installed
- [ ] Ports 8000, 5432, 6379 are available
- [ ] At least 4GB RAM available
- [ ] At least 10GB disk space available
- [ ] All project files are in the same directory
- [ ] No conflicting containers are running

## 🆘 Getting Help

If you're still experiencing issues:

1. **Run the test script**: `python test-docker.py`
2. **Check Docker logs**: `docker-compose logs`
3. **Verify system requirements**
4. **Try the simplified compose file**
5. **Check for conflicting services**

## 📞 Common Commands Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up -d --build

# Clean up everything
docker-compose down -v
docker system prune -a
```
