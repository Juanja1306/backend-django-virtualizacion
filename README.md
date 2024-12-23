# backend-django-virtualizacion
 Backend creado para las VM de google cloud
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
git --version
python3 --version
git clone https://github.com/Juanja1306/backend-django-virtualizacion
sudo apt install python3.11-venv -y
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# https
sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/django


server {
    listen 80;
    server_name 34.31.96.253;

    location / {
        return 301 https://$host$request_uri/;
    }
}

server {
    listen 443 ssl;
    server_name 34.31.96.253;

    ssl_certificate /etc/ssl/certs/selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/selfsigned.key;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}


sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
python manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem
