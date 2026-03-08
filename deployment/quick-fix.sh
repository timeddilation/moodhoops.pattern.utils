#!/bin/bash
# Quick fix script to resolve matplotlib permission and gunicorn issues

set -e

echo "========================================="
echo "Quick Fix for MoodHoops Service"
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

echo "Step 1: Creating matplotlib cache directory..."
mkdir -p $APP_DIR/.matplotlib
chown -R $APP_USER:$APP_USER $APP_DIR/.matplotlib

echo ""
echo "Step 2: Updating systemd service file..."
cp $APP_DIR/deployment/moodhoops-pattern-utils.service /etc/systemd/system/
systemctl daemon-reload

echo ""
echo "Step 3: Restarting service..."
systemctl restart moodhoops-pattern-utils

echo ""
echo "Step 4: Checking status..."
sleep 2
systemctl status moodhoops-pattern-utils --no-pager

echo ""
echo "========================================="
echo "Fix applied! ✅"
echo "========================================="
echo ""
echo "If you still see errors, check logs:"
echo "  sudo journalctl -u moodhoops-pattern-utils -n 50"
echo ""
