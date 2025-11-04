#!/bin/bash

# Pharmacy Management System Deployment Script
# Usage: ./deploy.sh [environment]
# Environment options: local, docker, production

set -e

ENVIRONMENT=${1:-local}
PROJECT_DIR=$(pwd)

echo "🏥 Deploying Pharmacy Management System - Environment: $ENVIRONMENT"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start within timeout"
    exit 1
}

case $ENVIRONMENT in
    "local")
        echo "🔧 Setting up local development environment..."
        
        # Check Python
        if ! command_exists python3; then
            echo "❌ Python 3 is required but not installed"
            exit 1
        fi
        
        # Install dependencies
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
        
        # Check MongoDB
        if ! command_exists mongod; then
            echo "⚠️  MongoDB not found. Please install MongoDB manually."
            echo "Ubuntu/Debian: sudo apt install mongodb"
            echo "macOS: brew install mongodb-community"
            exit 1
        fi
        
        # Start MongoDB if not running
        if ! pgrep mongod > /dev/null; then
            echo "🔄 Starting MongoDB..."
            sudo systemctl start mongod || mongod --fork --logpath /var/log/mongodb.log
        fi
        
        # Setup environment
        if [ ! -f ".env" ]; then
            echo "📝 Creating environment file..."
            cp .env.example .env
            echo "⚠️  Please edit .env file with your configuration"
        fi
        
        # Seed database
        echo "🌱 Seeding database..."
        python seed_database.py
        
        # Start services
        echo "🚀 Starting Flask API..."
        nohup python backend/app.py > flask.log 2>&1 &
        FLASK_PID=$!
        
        # Wait for API to be ready
        wait_for_service "http://localhost:5000/health" "Flask API"
        
        echo "🚀 Starting Streamlit frontend..."
        streamlit run app.py --server.port 8501 &
        STREAMLIT_PID=$!
        
        echo "✅ Local deployment complete!"
        echo "📱 Frontend: http://localhost:8501"
        echo "🔌 API: http://localhost:5000"
        echo "📊 API Health: http://localhost:5000/health"
        echo ""
        echo "🛑 To stop services:"
        echo "kill $FLASK_PID $STREAMLIT_PID"
        ;;
        
    "docker")
        echo "🐳 Setting up Docker environment..."
        
        # Check Docker
        if ! command_exists docker; then
            echo "❌ Docker is required but not installed"
            exit 1
        fi
        
        if ! command_exists docker-compose; then
            echo "❌ Docker Compose is required but not installed"
            exit 1
        fi
        
        # Setup environment
        if [ ! -f ".env" ]; then
            echo "📝 Creating environment file..."
            cp .env.example .env
            sed -i 's/localhost/mongodb/g' .env
        fi
        
        # Build and start services
        echo "🔨 Building Docker images..."
        docker-compose build
        
        echo "🚀 Starting services..."
        docker-compose up -d
        
        # Wait for services
        wait_for_service "http://localhost:5000/health" "Flask API"
        
        echo "🌱 Seeding database..."
        docker-compose exec api python seed_database.py
        
        echo "✅ Docker deployment complete!"
        echo "📱 Frontend: http://localhost:8501"
        echo "🔌 API: http://localhost:5000"
        echo "🐳 MongoDB: localhost:27017"
        echo ""
        echo "🛑 To stop services: docker-compose down"
        echo "📊 View logs: docker-compose logs -f"
        ;;
        
    "production")
        echo "🏭 Setting up production environment..."
        
        # Check requirements
        if ! command_exists docker; then
            echo "❌ Docker is required for production deployment"
            exit 1
        fi
        
        # Production environment check
        if [ ! -f ".env" ]; then
            echo "❌ Production .env file is required"
            echo "Please create .env file with production configuration"
            exit 1
        fi
        
        # SSL Certificate check
        if [ ! -d "ssl" ]; then
            echo "⚠️  SSL certificates not found. Creating self-signed certificates..."
            mkdir -p ssl
            openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/CN=localhost"
        fi
        
        # Deploy with production configuration
        echo "🚀 Deploying production services..."
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
        
        # Wait for services
        wait_for_service "http://localhost:5000/health" "Flask API"
        
        echo "🌱 Seeding database..."
        docker-compose exec api python seed_database.py
        
        echo "✅ Production deployment complete!"
        echo "🔒 HTTPS Frontend: https://localhost"
        echo "🔌 API: http://localhost:5000"
        echo "📊 Health Check: http://localhost:5000/health"
        echo ""
        echo "⚠️  Remember to:"
        echo "   - Configure proper SSL certificates"
        echo "   - Set up domain name and DNS"
        echo "   - Configure firewall rules"
        echo "   - Set up monitoring and backups"
        ;;
        
    *)
        echo "❌ Invalid environment: $ENVIRONMENT"
        echo "Usage: $0 [local|docker|production]"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment completed successfully!"
echo "📖 For more information, see DEPLOYMENT.md"