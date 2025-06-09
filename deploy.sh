#!/bin/bash

# Safe Companions Deployment Script for EC2 Ubuntu
# This script sets up and deploys the Safe Companions application

set -e

echo "🚀 Safe Companions Deployment Script"
echo "======================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please do not run this script as root"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker installed. Please log out and log back in for group changes to take effect."
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
fi

# Create production environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating production environment file..."
    cp .env.production .env
    
    # Generate a secure password
    SECURE_PASSWORD=$(openssl rand -base64 32)
    sed -i "s/your_secure_password_here/$SECURE_PASSWORD/g" .env
    
    echo "📝 Please review and update the .env file with your specific configuration"
    echo "   Especially update the DATABASE_PASSWORD if needed"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs

# Set up database schema
echo "🗄️  Setting up database..."
docker-compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database schema
echo "📋 Setting up database schema..."
docker-compose exec -T db psql -U postgres -d safecompanions < schema.sql || {
    echo "⚠️  Database schema setup failed. This might be normal if tables already exist."
}

# Build and start all services
echo "🏗️  Building and starting all services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test the application
echo "🧪 Testing application..."
if curl -f http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Access your application at:"
    echo "   - Local: http://localhost"
    echo "   - External: http://$(curl -s ifconfig.me)"
else
    echo "❌ Application test failed. Check logs with: docker-compose logs"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📚 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Update application: git pull && docker-compose up -d --build"
echo ""
echo "🔐 Default admin credentials:"
echo "   Email: admin@safecompanions.com"
echo "   Password: admin123"
echo ""
echo "⚠️  Remember to:"
echo "   1. Change default passwords"
echo "   2. Configure SSL certificates for production"
echo "   3. Set up proper firewall rules"
echo "   4. Configure domain name and DNS"

