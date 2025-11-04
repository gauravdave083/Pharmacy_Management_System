# Deployment Guide for Pharmacy Management System

## Overview
This guide covers multiple deployment options for the Pharmacy Management System.

## Prerequisites
- Docker and Docker Compose installed
- Git installed
- Domain name (for production deployment)
- SSL certificates (for HTTPS)

## Quick Start with Docker Compose

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd Pharmacy_Management_System
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start Services
```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Initialize Database
```bash
# Seed the database with initial data
docker-compose exec api python seed_database.py
```

### 5. Access Application
- Frontend: http://localhost:8501
- API: http://localhost:5000
- API Health: http://localhost:5000/health

## Production Deployment Options

### Option 1: Cloud VM Deployment (AWS/GCP/Azure)

#### AWS EC2 Deployment
```bash
# Launch EC2 instance (Ubuntu 22.04 LTS)
# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Clone repository
git clone <your-repo-url>
cd Pharmacy_Management_System

# Configure environment
cp .env.example .env
nano .env  # Set production values

# Deploy
docker-compose up -d

# Setup SSL with Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

#### Configure Nginx SSL
```bash
# Copy SSL certificates
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# Restart services
docker-compose restart nginx
```

### Option 2: Heroku Deployment

#### Backend (Flask API)
```bash
# Create Heroku app for API
heroku create pharmacy-api-app

# Add MongoDB Atlas addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set MONGODB_URI=$(heroku config:get MONGODB_URI)

# Deploy
git subtree push --prefix=backend heroku main
```

#### Frontend (Streamlit)
```bash
# Create Heroku app for frontend
heroku create pharmacy-frontend-app

# Set environment variables
heroku config:set API_BASE_URL=https://pharmacy-api-app.herokuapp.com

# Create Procfile for Streamlit
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main
```

### Option 3: Kubernetes Deployment

#### Create Kubernetes manifests
```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployments
kubectl get pods
kubectl get services
```

### Option 4: Railway Deployment

#### Backend
```bash
# Connect repository to Railway
# Set environment variables in Railway dashboard
# Deploy automatically on push
```

## Environment Variables

### Production Environment (.env)
```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secret-key-here

# Database
MONGODB_URI=mongodb://username:password@host:port/pharmacy_management

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# API Configuration
API_BASE_URL=https://api.yourdomain.com
```

## Database Migration

### MongoDB Atlas (Cloud Database)
```bash
# Export local data
mongodump --db pharmacy_management

# Import to Atlas
mongorestore --uri="mongodb+srv://username:password@cluster.mongodb.net/pharmacy_management" dump/pharmacy_management
```

## Monitoring and Maintenance

### Health Checks
```bash
# API Health
curl https://api.yourdomain.com/health

# Database Health
docker-compose exec mongodb mongo --eval "db.stats()"
```

### Backup Strategy
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec mongodb mongodump --db pharmacy_management --out /backup/backup_$DATE
```

### Log Management
```bash
# View application logs
docker-compose logs -f api
docker-compose logs -f frontend

# Rotate logs
docker-compose exec api logrotate /etc/logrotate.conf
```

## Security Considerations

1. **SSL/TLS**: Always use HTTPS in production
2. **Environment Variables**: Never commit secrets to version control
3. **Database Security**: Use strong passwords and network restrictions
4. **API Security**: Implement rate limiting and authentication
5. **Updates**: Keep dependencies updated regularly

## Scaling

### Horizontal Scaling
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  api:
    deploy:
      replicas: 3
  frontend:
    deploy:
      replicas: 2
```

### Load Balancing
- Use Nginx for load balancing multiple instances
- Consider using AWS ELB or GCP Load Balancer

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection**: Check MongoDB URI and network
3. **SSL issues**: Verify certificate paths and permissions
4. **Memory issues**: Increase container memory limits

### Debug Commands
```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs container_name

# Access container shell
docker-compose exec container_name bash

# Test API connectivity
curl -v http://localhost:5000/health
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Check GitHub issues
4. Contact support team

## Performance Optimization

### Frontend Optimization
- Enable Streamlit caching
- Optimize API calls
- Use pagination for large datasets

### Backend Optimization
- Implement database indexing
- Use connection pooling
- Add Redis for caching

### Database Optimization
- Create appropriate indexes
- Monitor query performance
- Regular maintenance tasks