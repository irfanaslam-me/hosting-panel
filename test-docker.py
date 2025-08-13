#!/usr/bin/env python3
"""
Docker Test Script for Hosting Panel
This script tests basic connectivity and configuration
"""

import os
import sys
import requests
import time
from urllib.parse import urlparse

def test_docker_connectivity():
    """Test if Docker is running and accessible"""
    print("🔍 Testing Docker connectivity...")
    
    try:
        import docker
        client = docker.from_env()
        info = client.info()
        print(f"✅ Docker is running (version: {info['ServerVersion']})")
        return True
    except Exception as e:
        print(f"❌ Docker connection failed: {e}")
        return False

def test_ports():
    """Test if required ports are available"""
    print("\n🔍 Testing port availability...")
    
    ports_to_test = [8000, 5432, 6379]
    
    for port in ports_to_test:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"⚠️  Port {port} is already in use")
            else:
                print(f"✅ Port {port} is available")
        except Exception as e:
            print(f"❌ Error testing port {port}: {e}")

def test_environment():
    """Test environment configuration"""
    print("\n🔍 Testing environment configuration...")
    
    required_vars = [
        'DATABASE_URL',
        'REDIS_URL',
        'SECRET_KEY',
        'ADMIN_USERNAME',
        'ADMIN_PASSWORD'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'password' in var.lower() or 'key' in var.lower():
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        db_url = os.getenv('DATABASE_URL', 'postgresql://hosting_user:hosting_password_123@localhost:5432/hosting_panel')
        parsed = urlparse(db_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database connected: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_redis_connection():
    """Test Redis connection"""
    print("\n🔍 Testing Redis connection...")
    
    try:
        import redis
        
        redis_url = os.getenv('REDIS_URL', 'redis://:redis_password_123@localhost:6379')
        r = redis.from_url(redis_url)
        
        # Test connection
        r.ping()
        print("✅ Redis connected successfully")
        return True
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Hosting Panel Docker Test Suite")
    print("=" * 40)
    
    # Test Docker
    docker_ok = test_docker_connectivity()
    
    # Test ports
    test_ports()
    
    # Test environment
    test_environment()
    
    # Test database (only if Docker is running)
    if docker_ok:
        print("\n⏳ Waiting for services to start...")
        time.sleep(5)
        
        db_ok = test_database_connection()
        redis_ok = test_redis_connection()
        
        if db_ok and redis_ok:
            print("\n🎉 All tests passed! Your Docker setup is working correctly.")
        else:
            print("\n⚠️  Some services failed. Check the logs above.")
    else:
        print("\n❌ Docker is not accessible. Please start Docker Desktop first.")
    
    print("\n📋 Next steps:")
    print("1. If Docker is not running, start Docker Desktop")
    print("2. Run: docker-compose up -d --build")
    print("3. Check logs: docker-compose logs -f")
    print("4. Access panel at: http://localhost:8000")

if __name__ == "__main__":
    main()
