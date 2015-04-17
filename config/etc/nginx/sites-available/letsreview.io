server {
    listen 80;
    server_name www.letsreview.io;
    rewrite ^/(.*) http://letsreview.io/$1 permanent;
}

server {
    listen 80;
    server_name letsreview.io;

    access_log /var/www/letsreview.io/logs/nginx/access.log;
    error_log /var/www/letsreview.io/logs/nginx/error.log;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_redirect off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/letsreview.io/html/r/static;
    }
}
