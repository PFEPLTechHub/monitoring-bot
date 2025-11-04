#!/bin/bash

# Monitoring Report Bot - Deployment Script for Hostinger VPS
# Run this script on your VPS after uploading the project files

set -e  # Exit on any error

echo "🚀 Starting Monitoring Report Bot Deployment..."
echo "================================================"

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
    print_warning "Running as root. Consider using a non-root user for security."
fi

# Set project directory
PROJECT_DIR="/var/www/monitoring-report-bot"
SERVICE_USER="www-data"

print_status "Setting up project directory: $PROJECT_DIR"

# Create project directory if it doesn't exist
sudo mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Install system dependencies
print_status "Installing system dependencies..."
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv postgresql-client mysql-client python3-dev libpq-dev build-essential git nginx supervisor

# Set up Python virtual environment
print_status "Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Set up file permissions
print_status "Setting up file permissions..."
sudo chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR
sudo chmod +x *.py

# Create logs directory
sudo mkdir -p /var/log
sudo touch /var/log/monitoring-report-bot.log
sudo chown $SERVICE_USER:$SERVICE_USER /var/log/monitoring-report-bot.log

# Create reports directory
mkdir -p reports
sudo chown $SERVICE_USER:$SERVICE_USER reports

# Set up supervisor configuration
print_status "Setting up supervisor configuration..."
sudo tee /etc/supervisor/conf.d/monitoring-report-bot.conf > /dev/null <<EOF
[program:monitoring-report-bot]
command=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/start_bot.py
directory=$PROJECT_DIR
user=$SERVICE_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/monitoring-report-bot.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
environment=PATH="$PROJECT_DIR/venv/bin"
EOF

# Reload supervisor
print_status "Reloading supervisor..."
sudo supervisorctl reread
sudo supervisorctl update

# Test the setup
print_status "Testing the setup..."
source venv/bin/activate
python test_connections.py

if [ $? -eq 0 ]; then
    print_status "✅ Setup test passed!"
else
    print_warning "⚠️  Setup test failed. Check your configuration."
fi

print_status "🎉 Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with database credentials"
echo "2. Start the bot: sudo supervisorctl start monitoring-report-bot"
echo "3. Check status: sudo supervisorctl status monitoring-report-bot"
echo "4. View logs: tail -f /var/log/monitoring-report-bot.log"
echo ""
echo "For more information, see DEPLOYMENT_HOSTINGER_VPS.md"
