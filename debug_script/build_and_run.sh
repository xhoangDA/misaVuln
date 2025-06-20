#!/bin/bash

# CVE Tools Docker Build & Run Script

echo "🚀 CVE Tools Docker Setup"
echo "========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build the Docker image
print_status "Building Docker image..."
docker build -t cve-tools:latest .

if [ $? -eq 0 ]; then
    print_status "Docker image built successfully!"
else
    print_error "Failed to build Docker image."
    exit 1
fi

# Start the services
print_status "Starting services with Docker Compose..."
docker-compose up -d

if [ $? -eq 0 ]; then
    print_status "Services started successfully!"
    echo ""
    print_status "🌐 Application URLs:"
    echo "   - Flask App: http://localhost:5000"
    echo "   - Nginx Proxy: http://localhost"
    echo "   - MySQL: localhost:3306"
    echo ""
    print_status "📋 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop services: docker-compose down"
    echo "   - Restart: docker-compose restart"
    echo "   - Shell access: docker exec -it cve_web bash"
    echo ""
    print_warning "Wait a few seconds for services to fully start up."
else
    print_error "Failed to start services."
    exit 1
fi
