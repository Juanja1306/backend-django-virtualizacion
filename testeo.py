from google.cloud import storage

from google.oauth2 import service_account # type: ignore

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    r"C:\Users\Juanja Malo\Desktop\backend-django-virtualizacion\backend_django\backend_django\inspiring-bonus-445203-p0-d3aab7b05921.json"
) 

client = storage.Client(credentials=GS_CREDENTIALS)
bucket = client.get_bucket('bucket-storage-backend')
# blob = bucket.blob('test.txt')
# blob.upload_from_string('This is a test!')
# print("File uploaded.")

image_path = r"C:\Users\Juanja Malo\Pictures\perro.jpg"  # Cambia esto a la ruta de tu imagen
blob_name = "perro.jpg"

# Crear un blob y subir la imagen
blob = bucket.blob(blob_name)
with open(image_path, "rb") as image_file:
    blob.upload_from_file(image_file, content_type="image/jpeg")  # Especifica el tipo de contenido

print(f"Imagen subida exitosamente: {blob.public_url}")