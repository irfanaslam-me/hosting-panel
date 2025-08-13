@echo off
echo 🔧 Docker Fix Script for Hosting Panel
echo ======================================

echo.
echo 📋 Checking Docker status...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Check Docker Compose version
echo.
echo 📋 Checking Docker Compose version...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not found!
    echo Trying 'docker compose' instead...
    docker compose --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Neither 'docker-compose' nor 'docker compose' found!
        echo Please install Docker Compose.
        pause
        exit /b 1
    ) else (
        echo ✅ Using 'docker compose' command
        set COMPOSE_CMD=docker compose
    )
) else (
    echo ✅ Using 'docker-compose' command
    set COMPOSE_CMD=docker-compose
)

echo.
echo 🧹 Cleaning up existing containers and volumes...
%COMPOSE_CMD% down -v >nul 2>&1

echo.
echo 🗑️  Cleaning Docker system...
docker system prune -f >nul 2>&1

echo.
echo 🔍 Checking for port conflicts...
netstat -ano | findstr :8000 >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Port 8000 is in use. Checking what's using it...
    netstat -ano | findstr :8000
    echo.
    echo Please stop the service using port 8000 or change the port in docker-compose.yml
    pause
)

echo.
echo 🚀 Starting services with simplified configuration...
%COMPOSE_CMD% -f docker-compose.simple.yml up -d --build

if errorlevel 1 (
    echo.
    echo ❌ Failed to start services. Trying alternative method...
    echo.
    echo 🐳 Starting services one by one...
    
    echo Starting PostgreSQL...
    %COMPOSE_CMD% -f docker-compose.simple.yml up -d postgres
    
    echo Waiting for PostgreSQL to be ready...
    timeout /t 15 /nobreak >nul
    
    echo Starting Redis...
    %COMPOSE_CMD% -f docker-compose.simple.yml up -d redis
    
    echo Waiting for Redis to be ready...
    timeout /t 10 /nobreak >nul
    
    echo Starting Hosting Panel...
    %COMPOSE_CMD% -f docker-compose.simple.yml up -d hosting_panel
)

echo.
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 Checking service status...
%COMPOSE_CMD% -f docker-compose.simple.yml ps

echo.
echo 📋 Recent logs:
%COMPOSE_CMD% -f docker-compose.simple.yml logs --tail=10

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access your hosting panel at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/api/docs
echo 🔑 Default login: admin / admin123
echo.
echo 📊 Monitor services: %COMPOSE_CMD% -f docker-compose.simple.yml ps
echo 📋 View logs: %COMPOSE_CMD% -f docker-compose.simple.yml logs -f
echo 🛑 Stop services: %COMPOSE_CMD% -f docker-compose.simple.yml down
echo.
pause
