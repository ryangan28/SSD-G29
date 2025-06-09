# Safe Companions - Secure Companion Platform

Safe Companions is a modern, private, and respectful platform that helps adults find trusted companions to connect with, whether for conversation, company at events, or simply spending quality time together.

## 🚀 Quick Start (EC2 Ubuntu Deployment)

### Prerequisites
- Ubuntu 20.04+ EC2 instance
- At least 2GB RAM and 10GB storage
- Security group allowing ports 80, 443, and 22

### One-Command Deployment
```bash
git clone <your-repository-url>
cd SSD-G29
./deploy.sh
```

The deployment script will automatically:
- Install Docker and Docker Compose
- Set up the database
- Build and start all services
- Configure SSL (with manual domain setup)

## 🏗️ Manual Deployment

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd SSD-G29
```

### 2. Configure Environment
```bash
cp .env.production .env
# Edit .env with your specific configuration
nano .env
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Set Up Database
```bash
# The database schema is automatically applied during startup
# Check logs if needed: docker-compose logs db
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_HOST`: Database host (use 'db' for Docker)
- `DATABASE_PORT`: Database port (default: 5432)
- `DATABASE_NAME`: Database name
- `DATABASE_USERNAME`: Database username
- `DATABASE_PASSWORD`: Database password (change from default!)
- `FLASK_ENV`: Environment (development/production)

### Default Credentials
- **Admin**: admin@safecompanions.com / admin123
- **Escort**: escort@example.com / password123
- **Seeker**: seeker@example.com / password123

⚠️ **Change these passwords immediately in production!**

## 🏛️ Architecture

### Services
- **Web Application**: Flask app with Gunicorn (Port 5000)
- **Database**: PostgreSQL 13 (Port 5432)
- **Reverse Proxy**: Nginx (Ports 80/443)
- **SSL**: Certbot for Let's Encrypt certificates

### Database Schema
- Users and profiles management
- Booking system
- Messaging system
- Payment tracking
- Review and rating system
- Admin audit logs

## 🔐 Security Features

### Implemented
- Password hashing (SHA-256)
- Session management
- Role-based access control (Admin, Escort, Seeker)
- SQL injection prevention (parameterized queries)
- HTTPS support (with proper SSL setup)

### Recommended Additional Security
- Enable firewall (UFW)
- Set up fail2ban
- Regular security updates
- Database backups
- Monitor logs

## 📊 Features

### For Seekers
- Browse escort profiles
- Filter by preferences
- Secure booking system
- Private messaging
- Payment processing
- Review and rating system

### For Escorts
- Profile management
- Availability scheduling
- Booking management
- Earnings tracking
- Client communication

### For Administrators
- User management
- Platform statistics
- Content moderation
- System monitoring

## 🛠️ Development

### Local Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up local database
sudo apt install postgresql
sudo -u postgres createdb safecompanions
sudo -u postgres psql -d safecompanions -f schema.sql

# Configure environment
export DATABASE_HOST=localhost
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=your_password
export DATABASE_NAME=safecompanions
export FLASK_ENV=development

# Run application
python app.py
```

### Project Structure
```
SSD-G29/
├── app.py                 # Main Flask application
├── controllers/           # Business logic controllers
├── data_sources/         # Database repositories
├── entities/             # Data models
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── nginx/                # Nginx configuration
├── schema.sql            # Database schema
├── docker-compose.yml    # Docker services
├── Dockerfile           # Application container
└── deploy.sh            # Deployment script
```

## 🔍 Monitoring and Logs

### View Application Logs
```bash
docker-compose logs -f web
```

### View Database Logs
```bash
docker-compose logs -f db
```

### View All Logs
```bash
docker-compose logs -f
```

### Service Status
```bash
docker-compose ps
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo lsof -i :80
   sudo lsof -i :443
   # Kill conflicting processes or change ports
   ```

2. **Database Connection Failed**
   ```bash
   docker-compose logs db
   # Check database credentials in .env
   ```

3. **SSL Certificate Issues**
   ```bash
   docker-compose logs certbot
   # Ensure domain points to your server
   ```

4. **Application Not Starting**
   ```bash
   docker-compose logs web
   # Check environment variables and dependencies
   ```

### Reset Everything
```bash
docker-compose down -v
docker system prune -a
./deploy.sh
```

## 📈 Scaling and Performance

### For High Traffic
- Use multiple web containers
- Set up database replication
- Implement Redis for sessions
- Use CDN for static assets
- Set up load balancer

### Monitoring
- Set up application monitoring (e.g., Prometheus)
- Database performance monitoring
- Log aggregation (e.g., ELK stack)
- Uptime monitoring

## 🔄 Updates and Maintenance

### Update Application
```bash
git pull
docker-compose up -d --build
```

### Database Backup
```bash
docker-compose exec db pg_dump -U postgres safecompanions > backup.sql
```

### Database Restore
```bash
docker-compose exec -T db psql -U postgres safecompanions < backup.sql
```

## 📞 Support

For technical support or questions:
1. Check the troubleshooting section
2. Review application logs
3. Check GitHub issues
4. Contact the development team

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Safe Companions** - Building connections with privacy and respect in mind.

