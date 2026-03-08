#!/bin/bash
# Quick setup script for MoodHoops Pattern Utils deployment

set -e  # Exit on any error

echo "========================================="
echo "MoodHoops Pattern Utils - Quick Setup"
echo "========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Variables
APP_DIR="/var/www/moodhoops-pattern-utils"
APP_USER="www-data"
LOG_DIR="/var/log/moodhoops-pattern-utils"

echo "Step 1: Installing system dependencies..."
apt update
apt install -y python3 python3-pip python3-venv nginx

echo ""
echo "Step 2: Creating directories..."
mkdir -p $LOG_DIR
chown -R $APP_USER:$APP_USER $LOG_DIR

echo ""
echo "Step 3: Setting up Python virtual environment..."
cd $APP_DIR
sudo -u $APP_USER python3 -m venv venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt

echo ""
echo "Step 4: Setting up systemd service..."
cp deployment/moodhoops-pattern-utils.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable moodhoops-pattern-utils

echo ""
echo "Step 5: Configuring nginx..."
cp deployment/nginx-moodhoops.conf /etc/nginx/sites-available/moodhoops

# Prompt for domain/IP
read -p "Enter your domain name or EC2 public IP: " DOMAIN
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/moodhoops

ln -sf /etc/nginx/sites-available/moodhoops /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

echo ""
echo "Step 6: Setting proper ownership..."
chown -R $APP_USER:$APP_USER $APP_DIR

echo ""
echo "Step 7: Starting services..."
systemctl start moodhoops-pattern-utils
systemctl restart nginx

echo ""
echo "========================================="
echo "Setup complete! 🎉"
echo "========================================="
echo ""
echo "Your application should now be running at:"
echo "  http://$DOMAIN"
echo ""
echo "Useful commands:"
echo "  Check app status:  sudo systemctl status moodhoops-pattern-utils"
echo "  View app logs:     sudo journalctl -u moodhoops-pattern-utils -f"
echo "  Restart app:       sudo systemctl restart moodhoops-pattern-utils"
echo "  Check nginx:       sudo systemctl status nginx"
echo ""
echo "Log files:"
echo "  Application: $LOG_DIR/error.log"
echo "  Nginx:       /var/log/nginx/moodhoops-error.log"
echo ""
