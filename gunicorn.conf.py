# Gunicorn configuration for UzIPTV

bind = "0.0.0.0:8000"
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%h %l %u %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'

# Process naming
proc_name = "uziptv"

# Server mechanics
daemon = False
pidfile = "/tmp/uziptv.pid"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "path/to/keyfile"
# certfile = "path/to/certfile"
