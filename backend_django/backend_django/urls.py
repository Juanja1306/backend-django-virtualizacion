
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from database import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subir/', views.subir_imagen, name='subir_imagen'),
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),
]
