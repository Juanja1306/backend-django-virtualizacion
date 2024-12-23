
# Backend para Google Cloud Virtual Machines (VM)

Esta guía detalla cómo configurar un backend en Django sobre una VM de Google Cloud, incluyendo la configuración de HTTP y HTTPS.

---

## 1. Preparación e instalación inicial

### Actualizamos y descargamos el proyecto
1. Actualiza el sistema y descarga el repositorio del proyecto:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install git -y
   git --version
   python3 --version
   git clone https://github.com/Juanja1306/backend-django-virtualizacion
   ```

2. Instala la versión correspondiente de Python y crea un entorno virtual:
   ```bash
   sudo apt install python3.11-venv -y
   python3 -m venv .venv
   ```

3. Activa el entorno virtual e instala las dependencias:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 2. Configuración de credenciales

1. Crea el archivo de credenciales:
   ```bash
   nano inspiring-bonus-445203-p0-d3aab7b05921.json
   ```

2. Encuentra la ubicación del archivo:
   ```bash
   find / -name "inspiring-bonus-445203-p0-d3aab7b05921.json" 2>/dev/null
   ```

3. Configura las credenciales en el archivo `settings.py`:
   - Abre `/home/usuario/backend-django-virtualizacion/backend_django/backend_django/settings.py`.
   - Añade lo siguiente, reemplazando la ruta del archivo:
     ```python
     GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
         r"/home/usuario/backend-django-virtualizacion/inspiring-bonus-445203-p0-d3aab7b05921.json"
     )
     ```

---

## 3. Pruebas en HTTP

1. Ejecuta el servidor:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. Prueba la API en Postman:
   ```
   http://<IP-EXTERNA>:8000/api/lista_imagenes/
   ```

---

## 4. Configuración de HTTPS

### Generar certificados SSL
1. Regresa a la carpeta del proyecto:
   ```bash
   cd /home/usuario/backend-django-virtualizacion
   ```

2. Crea los certificados SSL:
   ```bash
   sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

3. Instala y configura Nginx:
   ```bash
   sudo apt install nginx -y
   sudo nano /etc/nginx/sites-available/django
   ```

### Configuración de Nginx
Copia la siguiente configuración en el archivo de Nginx. Reemplaza la **IP externa** y las **rutas de los certificados**:

```nginx
server {
    listen 80;
    server_name <IP-EXTERNA>;

    location / {
        return 301 https://$host$request_uri/;
    }
}

server {
    listen 443 ssl;
    server_name <IP-EXTERNA>;

    ssl_certificate /home/<USUARIO>/backend-django-virtualizacion/cert.pem;
    ssl_certificate_key /home/<USUARIO>/backend-django-virtualizacion/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Habilitar la configuración de Nginx
1. Habilita el archivo de configuración:
   ```bash
   sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
   ```

2. Verifica la configuración:
   ```bash
   sudo nginx -t
   ```

3. Recarga Nginx:
   ```bash
   sudo systemctl reload nginx
   ```

4. Ejecuta el servidor con soporte HTTPS:
   ```bash
   python manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem
   ```

### Prueba en Postman
Accede a la API usando HTTPS:
```
https://<IP-EXTERNA>:8000/api/lista_imagenes/
```

---

## Notas finales
- Asegúrate de reemplazar `<IP-EXTERNA>` con la IP externa de tu VM.
- Mantén los certificados en una ubicación segura.
