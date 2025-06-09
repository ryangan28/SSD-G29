# Safe Companions - Windows 11 Docker Desktop Setup Guide

## 🖥️ Prerequisites for Windows 11

### 1. System Requirements
- Windows 11 (64-bit)
- At least 8GB RAM (16GB recommended)
- 20GB free disk space
- Virtualization enabled in BIOS/UEFI
- WSL 2 (Windows Subsystem for Linux)

### 2. Required Software
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- [Git for Windows](https://git-scm.com/download/win)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended)

## 🚀 Step-by-Step Setup

### Step 1: Install Docker Desktop

1. **Download Docker Desktop**
   ```
   https://www.docker.com/products/docker-desktop/
   ```

2. **Install Docker Desktop**
   - Run the installer as Administrator
   - Enable "Use WSL 2 instead of Hyper-V" option
   - Complete the installation and restart your computer

3. **Verify Docker Installation**
   ```cmd
   docker --version
   docker-compose --version
   ```

### Step 2: Enable WSL 2 (if not already enabled)

1. **Open PowerShell as Administrator**
   ```powershell
   wsl --install
   ```

2. **Set WSL 2 as default**
   ```powershell
   wsl --set-default-version 2
   ```

3. **Restart your computer**

### Step 3: Configure Docker Desktop

1. **Open Docker Desktop**
2. **Go to Settings → General**
   - ✅ Use the WSL 2 based engine
   - ✅ Start Docker Desktop when you log in

3. **Go to Settings → Resources → WSL Integration**
   - ✅ Enable integration with my default WSL distro
   - ✅ Enable integration with additional distros (if any)

4. **Apply & Restart Docker Desktop**

## 📁 Project Setup

### Step 1: Clone the Repository

1. **Open Command Prompt or PowerShell**
   ```cmd
   cd C:\
   mkdir Projects
   cd Projects
   git clone <your-repository-url> SSD-G29
   cd SSD-G29
   ```

### Step 2: Create Windows Environment File

1. **Copy the production environment template**
   ```cmd
   copy .env.production .env
   ```

2. **Edit the .env file** (use Notepad or VS Code)
   ```env
   # Database configuration (Docker service names)
   DATABASE_HOST=db
   DATABASE_PORT=5432
   DATABASE_NAME=safecompanions
   DATABASE_USERNAME=postgres
   DATABASE_PASSWORD=postgres123

   # Flask configuration
   FLASK_APP=app.py
   FLASK_ENV=development

   # Nginx configuration
   NGINX_CONF_FILE=nginx.dev.conf
   ```

### Step 3: Start the Application

1. **Open Command Prompt in project directory**
   ```cmd
   cd C:\Projects\SSD-G29
   ```

2. **Start all services**
   ```cmd
   docker-compose up -d
   ```

3. **Wait for services to start** (first time will take longer)
   ```cmd
   docker-compose logs -f
   ```

4. **Access the application**
   - Open browser: http://localhost
   - Or direct Flask app: http://localhost:5000

## 🔧 Windows-Specific Commands

### Docker Management
```cmd
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart web

# Rebuild and start
docker-compose up -d --build

# Remove everything (reset)
docker-compose down --volumes --rmi all --remove-orphans
```

### Database Access
```cmd
# Connect to PostgreSQL database
docker-compose exec db psql -U postgres -d safecompanions

# Or using external client
psql -h localhost -p 8888 -U postgres -d safecompanions
```

### File Editing
```cmd
# Open project in VS Code
code .

# Edit environment file
notepad .env

# View logs in real-time
docker-compose logs -f web
```

## 🐛 Common Windows Issues & Solutions

### Issue 1: Docker Desktop Won't Start
**Solution:**
1. Enable Virtualization in BIOS
2. Enable Windows features:
   ```cmd
   # Run as Administrator
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```
3. Restart computer

### Issue 2: Port Already in Use
**Solution:**
```cmd
# Find process using port 80
netstat -ano | findstr :80

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different ports in docker-compose.yml
```

### Issue 3: File Permission Issues
**Solution:**
```cmd
# Run Docker Desktop as Administrator
# Or change file permissions
icacls "C:\Projects\SSD-G29" /grant Everyone:F /T
```

### Issue 4: WSL 2 Issues
**Solution:**
```cmd
# Update WSL
wsl --update

# Restart WSL
wsl --shutdown
# Then restart Docker Desktop
```

## 📊 Development Workflow

### 1. Daily Development
```cmd
# Start development environment
cd C:\Projects\SSD-G29
docker-compose up -d

# View application logs
docker-compose logs -f web

# Make code changes (files are mounted, changes reflect immediately)

# Restart if needed
docker-compose restart web
```

### 2. Database Operations
```cmd
# View database logs
docker-compose logs -f db

# Access database
docker-compose exec db psql -U postgres -d safecompanions

# Reset database
docker-compose down -v
docker-compose up -d
```

### 3. Testing
```cmd
# Run tests (if available)
docker-compose exec web python -m pytest

# Check application health
curl http://localhost:5000
```

## 🔍 Monitoring & Debugging

### View Service Status
```cmd
docker-compose ps
```

### Check Resource Usage
```cmd
docker stats
```

### Access Container Shell
```cmd
# Access web application container
docker-compose exec web bash

# Access database container
docker-compose exec db bash
```

### View Detailed Logs
```cmd
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f --tail=100
```

## 🎯 Default Access Information

### Application URLs
- **Main Application**: http://localhost
- **Direct Flask App**: http://localhost:5000
- **Database**: localhost:8888

### Default Credentials
- **Admin**: admin@safecompanions.com / admin123
- **Escort**: escort@example.com / password123
- **Seeker**: seeker@example.com / password123

## 🔄 Update Process

### Update Application Code
```cmd
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Reset Everything
```cmd
# Complete reset
docker-compose down --volumes --rmi all --remove-orphans
docker system prune -a
docker-compose up -d --build
```

## 📝 Development Tips

### 1. File Watching
- Code changes are automatically reflected (volume mounting)
- No need to rebuild for Python code changes
- Restart required for configuration changes

### 2. Database Persistence
- Database data persists between restarts
- Use `docker-compose down -v` to reset database

### 3. Performance
- First startup takes longer (downloading images)
- Subsequent starts are much faster
- Consider allocating more resources to Docker Desktop

### 4. IDE Integration
- Use VS Code with Docker extension
- Python extension for syntax highlighting
- Remote containers extension for development inside containers

## 🆘 Getting Help

### Check Status
```cmd
# Docker Desktop status
docker version

# Service status
docker-compose ps

# System resources
docker system df
```

### Logs for Troubleshooting
```cmd
# Application logs
docker-compose logs web

# Database logs
docker-compose logs db

# All logs
docker-compose logs
```

### Reset if Stuck
```cmd
# Stop everything
docker-compose down

# Clean up
docker system prune

# Start fresh
docker-compose up -d --build
```

---

## ✅ Quick Start Summary

1. **Install Docker Desktop** and enable WSL 2
2. **Clone repository** to `C:\Projects\SSD-G29`
3. **Copy `.env.production` to `.env`**
4. **Run `docker-compose up -d`**
5. **Access http://localhost**

That's it! Your Safe Companions application should now be running on Windows 11 with Docker Desktop.

