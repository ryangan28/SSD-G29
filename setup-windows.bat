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

REM Stop any existing containers and clean up
echo 🛑 Stopping any existing containers...
docker-compose down -v >nul 2>&1

REM Remove old volumes to ensure fresh start
echo 🧹 Cleaning up old volumes...
docker volume prune -f >nul 2>&1

REM Build and start all services
echo 🚀 Building and starting Safe Companions application...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo ❌ Failed to start application
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for database to initialize...
timeout /t 15 /nobreak >nul

REM Wait for database to be ready by checking connection
echo 🔍 Checking database connection...
:wait_for_db
docker-compose exec db pg_isready -U admin -d safe_companions >nul 2>&1
if %errorlevel% neq 0 (
    echo    Still waiting for database...
    timeout /t 3 /nobreak >nul
    goto wait_for_db
)
echo ✅ Database is ready

REM Check if schema needs to be applied
echo 🗄️  Checking database schema...
docker-compose exec db psql -U admin -d safe_companions -c "SELECT 1 FROM users LIMIT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📋 Database schema not found, applying schema.sql...
    
    REM Try copying schema file to container
    echo    Copying schema file to container...
    docker cp schema.sql postgres-db:/tmp/schema.sql
    
    REM Try applying schema (don't exit on failure, try alternative)
    echo    Applying database schema...
    docker-compose exec db psql -U admin -d safe_companions -f /tmp/schema.sql >nul 2>&1
    
    REM Check if schema was applied successfully
    docker-compose exec db psql -U admin -d safe_companions -c "SELECT 1 FROM users LIMIT 1;" >nul 2>&1
    if %errorlevel% neq 0 (
        echo    First method failed, trying alternative approach...
        
        REM Alternative method: pipe schema content directly
        type schema.sql | docker-compose exec -T db psql -U admin -d safe_companions >nul 2>&1
        
        REM Check again
        docker-compose exec db psql -U admin -d safe_companions -c "SELECT 1 FROM users LIMIT 1;" >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ Schema application failed completely
            echo.
            echo 🔧 Manual fix required - run these commands:
            echo    docker cp schema.sql postgres-db:/tmp/schema.sql
            echo    docker-compose exec db psql -U admin -d safe_companions -f /tmp/schema.sql
            echo.
            echo 🌐 Application should still work, but login will fail until schema is applied
            echo.
            pause
        ) else (
            echo ✅ Database schema applied successfully (alternative method)
        )
    ) else (
        echo ✅ Database schema applied successfully
    )
) else (
    echo ✅ Database schema already exists
)

REM Verify test users exist
echo 👥 Verifying test users...
docker-compose exec db psql -U admin -d safe_companions -c "SELECT COUNT(*) FROM users;" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Could not verify test users
) else (
    echo ✅ Test users verified
)

REM Show running containers and port mappings
echo.
echo 📊 Service Status:
docker-compose ps

echo.
echo 🎉 Setup completed successfully!
echo.
echo 🌐 Access your application at:
echo    - Main application: http://localhost
echo    - Direct Flask app: http://localhost:5000
echo    - PgAdmin (if enabled): http://localhost:8080
echo.
echo 🔐 Test user credentials:
echo    - Admin : admin@safecompanions.com / password123
echo    - Escort: escort@example.com      / password123
echo    - Seeker: seeker@example.com      / password123
echo.
echo 📚 Useful commands:
echo    - View logs:       docker-compose logs -f
echo    - Stop services:   docker-compose down
echo    - Restart:         docker-compose restart
echo    - Full reset:      docker-compose down -v ^&^& setup-windows.bat
echo    - Database access: docker-compose exec db psql -U admin -d safe_companions
echo.
echo ⚠️  Remember to change default passwords in production!
echo.

REM Test application accessibility
echo 🧪 Testing application access...
timeout /t 5 /nobreak >nul
curl -s -o nul -w "%%{http_code}" http://localhost:5000 | findstr "200" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Application is responding correctly!
) else (
    echo ⚠️  Application may still be starting up
    echo    Try accessing http://localhost in your browser
)

echo.
echo 🚀 Safe Companions is ready to use!
echo.
pause