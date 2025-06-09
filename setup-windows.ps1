# Safe Companions - Windows PowerShell Setup Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Safe Companions - Windows Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    $dockerVersion = docker version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running or not installed" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if docker-compose is available
try {
    $composeVersion = docker-compose version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose not available"
    }
    Write-Host "✅ Docker Compose is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not available" -ForegroundColor Red
    Write-Host "Please ensure Docker Desktop is properly installed" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Create environment file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating environment file..." -ForegroundColor Yellow
    try {
        Copy-Item ".env.windows" ".env"
        Write-Host "✅ Environment file created" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create .env file" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✅ Environment file already exists" -ForegroundColor Green
}

# Stop any existing containers
Write-Host "🛑 Stopping any existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null

# Start the application
Write-Host "🚀 Starting Safe Companions application..." -ForegroundColor Yellow
$startResult = docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start application" -ForegroundColor Red
    Write-Host "Check the logs with: docker-compose logs" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check if services are running
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🎉 Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your application at:" -ForegroundColor Cyan
Write-Host "   - Main application: http://localhost" -ForegroundColor White
Write-Host "   - Direct Flask app: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "🔐 Default credentials:" -ForegroundColor Cyan
Write-Host "   - Admin: admin@safecompanions.com / admin123" -ForegroundColor White
Write-Host "   - Escort: escort@example.com / password123" -ForegroundColor White
Write-Host "   - Seeker: seeker@example.com / password123" -ForegroundColor White
Write-Host ""
Write-Host "📚 Useful commands:" -ForegroundColor Cyan
Write-Host "   - View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   - Stop application: docker-compose down" -ForegroundColor White
Write-Host "   - Restart: docker-compose restart" -ForegroundColor White
Write-Host "   - Reset everything: docker-compose down -v" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Remember to change default passwords in production!" -ForegroundColor Yellow
Write-Host ""

# Test application accessibility
Write-Host "🧪 Testing application..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Application is responding correctly!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Application responded with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not test application - it may still be starting up" -ForegroundColor Yellow
    Write-Host "   Try accessing http://localhost in your browser" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"

