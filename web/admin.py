from django.contrib import admin
from .models import Producto, Pedido, Entrega, Banner, Comunidad


from django.contrib import admin
from django.utils.html import format_html
from .models import Producto
from django.contrib import admin


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "slug", "mas_vendido")
    search_fields = ("nombre",)
    list_filter = ("mas_vendido",)
    list_editable = ("mas_vendido",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Comunidad)
class ComunidadAdmin(admin.ModelAdmin):
    list_display = ("titulo", "activo", "fecha_evento")
    search_fields = ("titulo",)





@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente")
    search_fields = ("cliente",)


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ("pedido", "nombre_recibe", "fecha", "domiciliario")
    search_fields = ("pedido__id", "nombre_recibe")
    list_filter = ("fecha", "domiciliario")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "activo", "orden")
    list_editable = ("activo", "orden")
    search_fields = ("titulo",)