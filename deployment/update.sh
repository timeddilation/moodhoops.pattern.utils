#!/bin/bash
# Update script for MoodHoops Pattern Utils

set -e  # Exit on any error

echo "========================================="
echo "MoodHoops Pattern Utils - Update"
echo "========================================="
echo ""

# Variables
APP_DIR="/var/www/moodhoops-pattern-utils"
APP_USER="www-data"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

echo "Step 1: Stopping the application..."
systemctl stop moodhoops-pattern-utils

echo ""
echo "Step 2: Pulling latest code..."
cd $APP_DIR

# Temporarily change ownership to current user for git operations
CURRENT_USER=$(logname 2>/dev/null || echo $SUDO_USER)
chown -R $CURRENT_USER:$CURRENT_USER $APP_DIR

# Pull as the current user
sudo -u $CURRENT_USER git pull

echo ""
echo "Step 3: Updating Python dependencies..."
# Change ownership back to www-data for pip operations
chown -R $APP_USER:$APP_USER $APP_DIR

# Ensure matplotlib cache directory exists
mkdir -p $APP_DIR/.matplotlib
chown -R $APP_USER:$APP_USER $APP_DIR/.matplotlib

# Update pip packages
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt --upgrade

echo ""
echo "Step 4: Restarting services..."
systemctl start moodhoops-pattern-utils
systemctl status moodhoops-pattern-utils --no-pager

echo ""
echo "========================================="
echo "Update complete!"
echo "========================================="
echo ""
echo "Check logs if needed:"
echo "  sudo journalctl -u moodhoops-pattern-utils -f"
echo ""
