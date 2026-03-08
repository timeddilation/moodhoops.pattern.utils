# Deployment Guide for MoodHoops Pattern Utils

This guide will help you deploy the MoodHoops Pattern Utils application on an EC2 instance with systemd and nginx.

## Prerequisites

- EC2 instance running Ubuntu 20.04 or later (Amazon Linux 2 also works with minor adjustments)
- SSH access to the instance
- Domain name or EC2 public IP address

## Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx
```

## Step 2: Create Application Directory

```bash
sudo mkdir -p /var/www/moodhoops-pattern-utils
# Temporarily give yourself ownership to upload files
sudo chown -R $USER:$USER /var/www/moodhoops-pattern-utils
```

## Step 3: Upload Application Files

From your local machine, upload the application to the EC2 instance:

```bash
# Using scp (replace with your EC2 details)
scp -r . ec2-user@your-ec2-ip:/var/www/moodhoops-pattern-utils/
```

Or clone from your git repository:

```bash
cd /var/www/moodhoops-pattern-utils
git clone <your-repo-url> .
```

## Step 4: Set Proper Ownership and Create Log Directory

```bash
# Change ownership to www-data (the user that will run the application)
sudo chown -R www-data:www-data /var/www/moodhoops-pattern-utils

# Create log directory
sudo mkdir -p /var/log/moodhoops-pattern-utils
sudo chown -R www-data:www-data /var/log/moodhoops-pattern-utils
```

## Step 5: Set Up Python Virtual Environment

```bash
cd /var/www/moodhoops-pattern-utils
# Run as www-data user since it owns the directory
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install --upgrade pip
sudo -u www-data venv/bin/pip install -r requirements.txt
```

## Step 6: Install and Configure systemd Service

```bash
# Copy the service file
sudo cp deployment/moodhoops-pattern-utils.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable moodhoops-pattern-utils

# Start the service
sudo systemctl start moodhoops-pattern-utils

# Check status
sudo systemctl status moodhoops-pattern-utils
```

## Step 7: Configure Nginx

```bash
# Copy the nginx configuration
sudo cp deployment/nginx-moodhoops.conf /etc/nginx/sites-available/moodhoops

# Edit the configuration to set your domain or IP
sudo nano /etc/nginx/sites-available/moodhoops
# Change 'server_name your-domain.com;' to your actual domain or EC2 public IP

# Create symbolic link to enable the site
sudo ln -s /etc/nginx/sites-available/moodhoops /etc/nginx/sites-enabled/

# Remove default nginx site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## Step 8: Configure Security Group (AWS)

In your EC2 instance's security group, ensure the following ports are open:
- Port 80 (HTTP)
- Port 22 (SSH - for management)
- Port 443 (HTTPS - if using SSL)

## Step 9: Access Your Application

Open your browser and navigate to:
- `http://your-domain.com` or `http://your-ec2-public-ip`

## Useful Commands

### Check Application Logs

```bash
# Application logs
sudo journalctl -u moodhoops-pattern-utils -f

# Gunicorn logs
sudo tail -f /var/log/moodhoops-pattern-utils/error.log
sudo tail -f /var/log/moodhoops-pattern-utils/access.log

# Nginx logs
sudo tail -f /var/log/nginx/moodhoops-error.log
sudo tail -f /var/log/nginx/moodhoops-access.log
```

### Restart Services

```bash
# Restart application
sudo systemctl restart moodhoops-pattern-utils

# Restart nginx
sudo systemctl restart nginx
```

### Update Application Code

**Option 1: Use the update script (recommended)**
```bash
cd /var/www/moodhoops-pattern-utils
sudo bash deployment/update.sh
```

**Option 2: Manual update**
```bash
cd /var/www/moodhoops-pattern-utils

# Stop the service
sudo systemctl stop moodhoops-pattern-utils

# Fix git ownership and pull
sudo chown -R $USER:$USER /var/www/moodhoops-pattern-utils
git pull

# Update dependencies as www-data
sudo chown -R www-data:www-data /var/www/moodhoops-pattern-utils
sudo -u www-data /var/www/moodhoops-pattern-utils/venv/bin/pip install -r requirements.txt --upgrade

# Restart
sudo systemctl start moodhoops-pattern-utils
```

## Optional: Set Up SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Certbot will automatically configure nginx for HTTPS
# and set up automatic renewal
```

## Troubleshooting

### Service won't start
- Check logs: `sudo journalctl -u moodhoops-pattern-utils -n 50`
- Verify Python path: `which python3` in the venv
- Check file permissions: `ls -la /var/www/moodhoops-pattern-utils`

### 502 Bad Gateway
- Check if gunicorn is running: `sudo systemctl status moodhoops-pattern-utils`
- Check gunicorn logs for errors
- Verify the bind address matches in systemd service and nginx config

### Permission Issues
```bash
sudo chown -R www-data:www-data /var/www/moodhoops-pattern-utils
sudo chown -R www-data:www-data /var/log/moodhoops-pattern-utils
```

### Git "dubious ownership" error
If you get a git error about dubious ownership when trying to pull:
```bash
# Temporarily change ownership to your user for git operations
sudo chown -R $USER:$USER /var/www/moodhoops-pattern-utils
git pull
# Change back to www-data
sudo chown -R www-data:www-data /var/www/moodhoops-pattern-utils
```

Or use the update script which handles this automatically:
```bash
sudo bash deployment/update.sh
```

## Performance Tuning

For better performance on larger EC2 instances, adjust the number of workers in `deployment/gunicorn_config.py`:
- Workers: `(2 x number_of_cores) + 1`
- For t2.micro: 3 workers
- For t2.small: 3 workers
- For t2.medium: 5 workers
