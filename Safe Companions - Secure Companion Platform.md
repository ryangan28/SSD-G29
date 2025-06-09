# Safe Companions - Secure Companion Platform

A modern, private, and respectful platform that helps adults find trusted companions to connect with, whether for conversation, company at events, or simply spending quality time together.

## ✨ Features

- **Secure User Management**: Role-based access for Admins, Escorts, and Seekers
- **Profile System**: Comprehensive profiles with verification status
- **Booking Management**: Secure booking system with status tracking
- **Messaging**: Private, encrypted communication between users
- **Payment Processing**: Integrated payment tracking and management
- **Review System**: Rating and review system for quality assurance
- **Admin Dashboard**: Complete platform management and analytics

## 🚀 Quick Deployment

### EC2 Ubuntu (Recommended for Production)
```bash
git clone <repository-url>
cd SSD-G29
./deploy.sh
```

### Windows Development
```bat
# Install Python 3.11+, Docker Desktop, PostgreSQL Client
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🏛️ Architecture

- **Backend**: Flask with PostgreSQL database
- **Frontend**: Responsive HTML templates with Bootstrap
- **Deployment**: Docker containers with Nginx reverse proxy
- **Security**: Session management, password hashing, role-based access

## 🔐 Default Credentials

- **Admin**: admin@safecompanions.com / admin123
- **Escort**: escort@example.com / password123  
- **Seeker**: seeker@example.com / password123

⚠️ **Change these passwords immediately in production!**

## 📊 Tech Stack

- **Backend**: Python 3.11, Flask, PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap, JavaScript
- **Deployment**: Docker, Docker Compose, Nginx
- **Security**: SHA-256 hashing, session management, HTTPS

## 🛠️ Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (for containerized deployment)

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd SSD-G29

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export DATABASE_HOST=localhost
export DATABASE_NAME=safecompanions
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=your_password
export FLASK_ENV=development

# Set up database
sudo -u postgres createdb safecompanions
sudo -u postgres psql -d safecompanions -f schema.sql

# Run application
python app.py
```

## 🐳 Docker Deployment

### Development
```bash
# Create environment file
cp .env.production .env
# Edit .env with your configuration

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production
```bash
# Use production environment
docker-compose --env-file .env.production up -d --build

# Stop services
docker-compose --env-file .env.production down
```

### Database Access
```bash
# Connect to PostgreSQL in container
psql -h localhost -p 8888 -U postgres -d safecompanions
```

## 📁 Project Structure

```
SSD-G29/
├── app.py                 # Main Flask application
├── controllers/           # Business logic
│   └── auth_controller.py
├── data_sources/         # Database access layer
│   ├── repositories.py
│   └── unit_of_work.py
├── entities/             # Data models
│   └── user.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard-html-page.html
│   ├── profile-html-page.html
│   └── ...
├── static/               # Static assets
│   └── css/
├── nginx/                # Nginx configuration
├── schema.sql            # Database schema
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Application container
├── deploy.sh            # Deployment script
├── requirements.txt      # Python dependencies
├── requirements-prod.txt # Production dependencies
└── DEPLOYMENT.md        # Detailed deployment guide
```

## 🔍 Key Components

### Authentication & Authorization
- Session-based authentication
- Role-based access control (RBAC)
- Password hashing and validation

### Database Layer
- PostgreSQL with connection pooling
- Repository pattern for data access
- Comprehensive schema with relationships

### User Interface
- Responsive design for mobile and desktop
- Role-specific dashboards
- Real-time status updates

### Security Features
- Input validation and sanitization
- SQL injection prevention
- Secure session management
- HTTPS support

## 📈 Monitoring and Maintenance

### View Logs
```bash
docker-compose logs -f web    # Application logs
docker-compose logs -f db     # Database logs
docker-compose logs -f nginx  # Nginx logs
```

### Service Management
```bash
docker-compose ps            # Check service status
docker-compose restart web   # Restart application
docker-compose down -v       # Stop and remove volumes
```

### SSL Certificate Management
```bash
# Check certificate status
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run

# Check renewal timer
systemctl list-timers | grep certbot
```

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U postgres safecompanions > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres safecompanions < backup.sql
```

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports 80, 443, 5000, 5432 are available
2. **Database connection**: Verify credentials in .env file
3. **SSL issues**: Ensure domain points to your server IP
4. **Permission errors**: Check file permissions and Docker group membership

### Reset Everything
```bash
docker-compose down --volumes --rmi all --remove-orphans
./deploy.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For technical support:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
2. Review application logs
3. Check GitHub issues
4. Contact the development team

---

Built with ❤️ for secure and respectful connections.

