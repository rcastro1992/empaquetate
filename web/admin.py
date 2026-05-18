from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    Producto,
    Pedido,
    Entrega,
    Banner,
    Comunidad,
    Testimonio,
    InformacionEmpresa,
    GaleriaEmpresa,
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "activo", "orden")
    list_editable = ("activo", "orden")
    search_fields = ("titulo",)

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
    # Añadimos 'repartidor_asignado' para que lo veas en la tabla principal
    list_display = ('id', 'cliente', 'direccion', 'ciudad', 'fecha_pedido', 'estado', 'repartidor_asignado')
    
    # Esto te permite asignar repartidor y cambiar estado desde la lista (muy rápido)
    list_editable = ('estado', 'repartidor_asignado')
    
    # Filtros laterales para que sepas qué tiene cada domiciliario
    list_filter = ('ciudad', 'estado', 'repartidor_asignado')
    
    search_fields = ('cliente', 'direccion', 'ciudad')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    # Mostramos la firma y las fotos en el listado si quieres
    list_display = ("pedido", "nombre_recibe", "fecha_local", "domiciliario", "ver_foto")
    list_filter = ("fecha", "domiciliario")
    search_fields = ("pedido__id", "nombre_recibe")
    
    # Campos que no se pueden editar manualmente por seguridad
    readonly_fields = ("fecha", "firma")

    def fecha_local(self, obj):
        fecha = timezone.localtime(obj.fecha)
        return fecha.strftime("%d/%m/%Y %I:%M %p")
    fecha_local.short_description = "Fecha (Hora local)"

    # Pequeño truco para ver una miniatura de la foto en el admin
    def ver_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 50px; height:auto;">', obj.foto.url)
        return "Sin foto"
    ver_foto.short_description = "Prueba de entrega"

    # web/admin.py


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'destacado_inicio', 'fecha')
    list_editable = ('activo', 'destacado_inicio')

@admin.register(InformacionEmpresa)
class InformacionEmpresaAdmin(admin.ModelAdmin):

    fieldsets = (

        ("SECCIÓN PRINCIPAL", {
            'fields': (
                'hero_titulo',
                'hero_descripcion',
                'hero_imagen',
                'hero_video',
                'hero_video_url',
            )
        }),

        ("HISTORIA EMPRESARIAL", {
            'fields': (
                'historia_titulo',
                'historia_descripcion',
                'historia_imagen',
            )
        }),

        ("CÓMO TRABAJAMOS", {
            'fields': (
                'trabajo_titulo',
                'trabajo_descripcion',
                'trabajo_video',
                'trabajo_video_url',
            )
        }),

        ("INFORMACIÓN CORPORATIVA", {
            'fields': (
                'mision',
                'vision',
                'objetivo',
            )
        }),

        ("CONFIGURACIÓN", {
            'fields': (
                'activo',
            )
        }),
    )

    list_display = (
        'id',
        'hero_titulo',
        'activo',
    )


@admin.register(GaleriaEmpresa)
class GaleriaEmpresaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'titulo',
        'activo',
        'fecha',
    )

