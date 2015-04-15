import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = "/tmp/review.pid"
accesslog = "/var/www/letsreview.io/logs/gunicorn/access.log"
errorlog = "/var/www/letsreview.io/logs/gunicorn/error.log"
