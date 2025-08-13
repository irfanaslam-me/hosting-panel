#!/bin/bash

# Hosting Panel Docker Startup Script
echo "🚀 Starting Modern Hosting Panel with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo ""
echo "✅ Hosting Panel is starting up!"
echo "🌐 Access the panel at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo "🔑 Default admin credentials: admin / admin123"
echo ""
echo "📊 Monitor services with: docker-compose ps"
echo "📋 View logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
