@echo off
echo 🚀 Starting Modern Hosting Panel with Docker...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Build and start services
echo 📦 Building and starting services...
docker-compose up -d --build

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check service status
echo 🔍 Checking service status...
docker-compose ps

REM Show logs
echo 📋 Recent logs:
docker-compose logs --tail=20

echo.
echo ✅ Hosting Panel is starting up!
echo 🌐 Access the panel at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/api/docs
echo 🔑 Default admin credentials: admin / admin123
echo.
echo 📊 Monitor services with: docker-compose ps
echo 📋 View logs with: docker-compose logs -f
echo 🛑 Stop services with: docker-compose down
echo.
pause
