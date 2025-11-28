# En C:\...\empaquetate\web\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('compania/', views.compania, name='compania'),
    path('contacto/', views.contacto, name='contacto'),
    path('intranet/', views.intranet, name='intranet'),
    path('producto/<slug:slug_producto>/', views.detalle_producto, name='detalle_producto'),
    ]