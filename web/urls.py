# web/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('compania/', views.compania, name='compania'),
    path('contacto/', views.contacto, name='contacto'),

    # INTRANET (confirmar entrega)
    path('intranet/', views.intranet, name='intranet'),

    # # Esta URL ya NO debe duplicar nombre
    # path('confirmar-entrega/', views.intranet, name='confirmar_entrega'),

    path('producto/<slug:slug_producto>/', views.detalle_producto, name='detalle_producto'),
]
