"""Gunicorn configuration file for MoodHoops Pattern Utils."""

import multiprocessing

# Bind address
bind = "127.0.0.1:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/var/log/moodhoops-pattern-utils/access.log"
errorlog = "/var/log/moodhoops-pattern-utils/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "moodhoops-pattern-utils"

# Server mechanics
daemon = False
pidfile = "/var/run/moodhoops-pattern-utils.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
