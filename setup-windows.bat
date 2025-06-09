@echo off
echo.
echo ========================================
echo  Safe Companions - Windows Setup
echo ========================================
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running or not installed
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)
echo ✅ Docker is running

REM Check if docker-compose is available
docker-compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available
    echo Please ensure Docker Desktop is properly installed
    pause
    exit /b 1
)
echo ✅ Docker Compose is available

REM Create environment file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment file...
    copy .env.windows .env
    if %errorlevel% neq 0 (
        echo ❌ Failed to create .env file
        pause
        exit /b 1
    )
    echo ✅ Environment file created
) else (
    echo ✅ Environment file already exists
)

REM Stop any existing containers
echo 🛑 Stopping any existing containers...
docker-compose down >nul 2>&1

REM Build and start all services (including web under pgadmin profile)
echo 🚀 Building and starting Safe Companions application...
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile pgadmin up -d --build

if %errorlevel% neq 0 (
    echo ❌ Failed to start application
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for services to initialize...
timeout /t 15 /nobreak >nul

REM Show running containers and port mappings
docker ps

echo.
echo 🎉 Setup completed!
echo.
echo 🌐 Access your application at:
echo    - Via nginx proxy: http://localhost
echo    - Direct Flask app: http://localhost:5000
echo.
echo 🔐 Default credentials:
echo    - Admin : admin@safecompanions.com / admin123
echo    - Escort: escort@example.com      / password123
echo    - Seeker: seeker@example.com      / password123
echo.
echo 📚 Useful commands:
echo    - View logs:     docker-compose logs -f
echo    - Stop services: docker-compose down
echo    - Restart:       docker-compose restart
echo    - Full reset:    docker-compose down -v
echo.
echo ⚠️  Remember to change default passwords in production!
echo.
pause
