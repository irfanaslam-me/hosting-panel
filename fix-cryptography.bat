@echo off
echo 🔧 Fixing Cryptography Package Issue
echo ====================================

echo.
echo 📋 The issue is with the cryptography package version...
echo.

echo 🧹 Cleaning up existing containers and images...
docker-compose down -v >nul 2>&1
docker system prune -f >nul 2>&1

echo.
echo 📦 Rebuilding with updated requirements...
echo.

echo ✅ Using updated requirements.txt with cryptography>=42.0.0
echo ✅ Using flexible version constraints (>= instead of ==)
echo.

echo 🚀 Starting build process...
docker-compose -f docker-compose.simple.yml up -d --build

if errorlevel 1 (
    echo.
    echo ❌ Build failed. Trying alternative approach...
    echo.
    echo 🔄 Building image manually first...
    docker build -t hosting_panel .
    
    if errorlevel 1 (
        echo.
        echo ❌ Manual build also failed. 
        echo.
        echo 📋 Common solutions:
        echo 1. Update Docker Desktop to latest version
        echo 2. Ensure you have at least 4GB RAM allocated to Docker
        echo 3. Try running: docker system prune -a
        echo 4. Check if your antivirus is blocking Docker
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo ✅ Manual build successful! Starting services...
        docker-compose -f docker-compose.simple.yml up -d
    )
) else (
    echo.
    echo ✅ Build successful!
)

echo.
echo ⏳ Waiting for services to be ready...
timeout /t 15 /nobreak >nul

echo.
echo 🔍 Checking service status...
docker-compose -f docker-compose.simple.yml ps

echo.
echo 📋 Recent logs:
docker-compose -f docker-compose.simple.yml logs --tail=10

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access your hosting panel at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/api/docs
echo 🔑 Default login: admin / admin123
echo.
pause
