server {
    listen 80;
    server_name easy-text.ru;
    location / {
        proxy_pass http://localhost:3000;
    }
    location ~ ^/api/(.*)$ {
        proxy_pass http://0.0.0.0:8080/$1;
    }
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
}
