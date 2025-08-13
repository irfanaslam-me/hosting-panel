#!/bin/bash

# Modern Hosting Panel Installation Script
# This script installs all dependencies and sets up the hosting panel

set -e

echo "🚀 Installing Modern Hosting Panel..."

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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt-get update

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    mysql-server \
    php8.1-fpm \
    php8.1-mysql \
    php8.1-curl \
    php8.1-gd \
    php8.1-mbstring \
    php8.1-xml \
    php8.1-zip \
    certbot \
    python3-certbot-nginx \
    docker.io \
    docker-compose \
    redis-server \
    git \
    curl \
    wget \
    unzip \
    tar \
    gzip

# Start and enable services
print_status "Starting and enabling services..."
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl start mysql
sudo systemctl enable mysql
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl start docker
sudo systemctl enable docker

# Create application directory
print_status "Creating application directory..."
sudo mkdir -p /var/www/hosting-panel
sudo chown $USER:$USER /var/www/hosting-panel

# Create Python virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv /var/www/hosting-panel/venv
source /var/www/hosting-panel/venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating necessary directories..."
sudo mkdir -p /var/www/websites
sudo mkdir -p /var/backups/hosting-panel
sudo mkdir -p /var/log/hosting-panel
sudo chown -R $USER:$USER /var/www/websites
sudo chown -R $USER:$USER /var/backups/hosting-panel
sudo chown -R $USER:$USER /var/log/hosting-panel

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/hosting-panel > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static/ {
        alias /var/www/hosting-panel/app/static/;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/hosting-panel /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Configure MySQL
print_status "Configuring MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hosting_panel;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'hosting_panel'@'localhost' IDENTIFIED BY 'hosting_panel_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON hosting_panel.* TO 'hosting_panel'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/hosting-panel.service > /dev/null <<EOF
[Unit]
Description=Modern Hosting Panel
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=/var/www/hosting-panel
Environment=PATH=/var/www/hosting-panel/venv/bin
ExecStart=/var/www/hosting-panel/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable hosting-panel

# Create environment file
print_status "Creating environment configuration..."
tee /var/www/hosting-panel/.env > /dev/null <<EOF
# Modern Hosting Panel Configuration
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=mysql://hosting_panel:hosting_panel_password@localhost/hosting_panel
WEB_SERVER=nginx
CERTBOT_EMAIL=admin@localhost
ADMIN_PASSWORD=admin123
EOF

# Set proper permissions
sudo chown -R $USER:$USER /var/www/hosting-panel
sudo chmod +x /var/www/hosting-panel/main.py

# Start the application
print_status "Starting the hosting panel..."
sudo systemctl start hosting-panel

# Wait a moment for the service to start
sleep 5

# Check if the service is running
if sudo systemctl is-active --quiet hosting-panel; then
    print_status "✅ Modern Hosting Panel is running successfully!"
    print_status "🌐 Access the panel at: http://$(hostname -I | awk '{print $1}')"
    print_status "👤 Default admin credentials:"
    print_status "   Username: admin"
    print_status "   Password: admin123"
    print_warning "⚠️  Please change the default password after first login!"
else
    print_error "❌ Failed to start the hosting panel. Check the logs:"
    print_error "   sudo journalctl -u hosting-panel -f"
    exit 1
fi

# Display useful commands
echo ""
print_status "Useful commands:"
echo "  Start/Stop: sudo systemctl start/stop hosting-panel"
echo "  Status: sudo systemctl status hosting-panel"
echo "  Logs: sudo journalctl -u hosting-panel -f"
echo "  Restart: sudo systemctl restart hosting-panel"
echo ""

print_status "🎉 Installation completed successfully!"
print_warning "Remember to:"
print_warning "1. Change the default admin password"
print_warning "2. Configure SSL certificates for production"
print_warning "3. Set up proper firewall rules"
print_warning "4. Configure backup strategies" 