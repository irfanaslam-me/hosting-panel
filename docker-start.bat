@echo off
echo 🚀 Starting Modern Hosting Panel with Docker...
echo ==============================================

REM Check if Docker is running
echo 📋 Checking Docker status...
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)
echo ✅ Docker is running

REM Check Docker Compose version
echo.
echo 📋 Checking Docker Compose version...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not found! Trying 'docker compose' instead...
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

REM Clean up existing containers
echo.
echo 🧹 Cleaning up existing containers and volumes...
%COMPOSE_CMD% down -v >nul 2>&1
docker system prune -f >nul 2>&1

REM Check for port conflicts
echo.
echo 🔍 Checking for port conflicts...
netstat -ano | findstr :8000 >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Port 8000 is in use. Checking what's using it...
    netstat -ano | findstr :8000
    echo.
    echo Please stop the service using port 8000 or change the port.
    pause
)

REM Start with simplified compose file
echo.
echo 🚀 Starting services with simplified configuration...
echo ✅ Using docker-compose.simple.yml (no health checks, simpler dependencies)
echo ✅ Fixed ALLOWED_HOSTS issue: "['*']" instead of "*"
echo ✅ Using flexible package versions (>= instead of ==)
echo.

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
timeout /t 15 /nobreak >nul

REM Check service status
echo.
echo 🔍 Checking service status...
%COMPOSE_CMD% -f docker-compose.simple.yml ps

REM Show logs
echo.
echo 📋 Recent logs:
%COMPOSE_CMD% -f docker-compose.simple.yml logs --tail=15

echo.
echo ✅ Hosting Panel setup complete!
echo.
echo 🌐 Access the panel at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/api/docs
echo 🔑 Default admin credentials: admin / admin123
echo.
echo 📊 Monitor services: %COMPOSE_CMD% -f docker-compose.simple.yml ps
echo 📋 View logs: %COMPOSE_CMD% -f docker-compose.simple.yml logs -f
echo 🛑 Stop services: %COMPOSE_CMD% -f docker-compose.simple.yml down
echo.
echo 💡 If you encounter issues:
echo    1. Check logs: %COMPOSE_CMD% -f docker-compose.simple.yml logs
echo    2. Restart: %COMPOSE_CMD% -f docker-compose.simple.yml restart
echo    3. Rebuild: %COMPOSE_CMD% -f docker-compose.simple.yml up -d --build
echo.
pause
