from django.shortcuts import render, redirect # type: ignore
from .forms import ImagenForm
from .models import Imagen
from django.core.files.storage import default_storage # type: ignore
from google.cloud import storage
from backend_django.settings import bucket


def subir_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST)
        if form.is_valid():
            try:
                # Configuración del cliente de Google Cloud Storage

                # Subir la imagen al bucket
                archivo = request.FILES['archivo']  # El archivo subido por el usuario
                blob_name = archivo.name
                blob = bucket.blob(blob_name)

                # Subir el archivo al bucket
                blob.upload_from_file(archivo.file, content_type=archivo.content_type)

                # Guardar la URL pública en el modelo
                imagen = form.save(commit=False)  # Guarda el modelo pero no en la BD
                imagen.url = blob.public_url  # Asigna la URL pública generada
                imagen.save()  # Guarda en la base de datos

                print("Imagen subida y guardada correctamente.")
                print(f"URL de la imagen: {imagen.url}")
                return redirect('lista_imagenes')
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")
        else:
            print(f"Errores del formulario: {form.errors}")
    else:
        form = ImagenForm()
    return render(request, 'database/subir_imagen.html', {'form': form})


def lista_imagenes(request):
    imagenes = Imagen.objects.all()
    print(f"Backend de almacenamiento: {default_storage.__class__.__name__}")
    return render(request, 'database/lista_imagenes.html', {'imagenes': imagenes})
