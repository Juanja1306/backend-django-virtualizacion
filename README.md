# Backend creado para las VM de google cloud
## Actualizamos y descargamos el proyecto (Cambiamos python3.11 por la version de py correspondiente)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
git --version
python3 --version
git clone https://github.com/Juanja1306/backend-django-virtualizacion
sudo apt install python3.11-venv -y
python3 -m venv .venv
pip install -r requirements.txt
```

Creamos las credenciales 
```bash
nano inspiring-bonus-445203-p0-d3aab7b05921.json
```

Necesitamos ver la ubicacion del archivo 
```bash
find / -name "inspiring-bonus-445203-p0-d3aab7b05921.json" 2>/dev/null
```

Esa ubicacion la pegamos en el archivo "/home/usuario/backend-django-virtualizacion/backend_django/backend_django/settings.py" 
```bash
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    r"/home/usuario/backend-django-virtualizacion/inspiring-bonus-445203-p0-d3aab7b05921.json"
)
```
Por ultimo probamos el http
```bash
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```
Probamos en el postman
http://< ip-externa >:8000/api/lista_imagenes/

---

## HTTPS
```bash
sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/django
```

Ponemos la configuracion en el nano y cambiamos la ip externa (34.31.96.253 por la ip externa de la VM) y cambiar la direccion de las llaves creadas (/home/usuario/backend-django-virtualizacion/cert.pem y /home/usuario/backend-django-virtualizacion/key.pem)
```bash
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

    ssl_certificate /home/usuario/backend-django-virtualizacion/cert.pem;
    ssl_certificate_key /home/usuario/backend-django-virtualizacion/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Reiniciamos y probamos el https
```bash
sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
python manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem
```
