from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# =========================================================
# BANNERS
# =========================================================
class Banner(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='banners/')
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo if self.titulo else f"Banner {self.id}"

    class Meta:
        ordering = ('orden',)


# =========================================================
# PRODUCTOS
# =========================================================
class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    descripcion = models.TextField(blank=True, null=True)

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    referencia = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    colores = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    medidas = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    mas_vendido = models.BooleanField(default=False)

    unidades_disponibles = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    @property
    def colores_lista(self):
        if self.colores:
            return [
                c.strip()
                for c in self.colores.split(",")
                if c.strip()
            ]
        return []


# =========================================================
# COMUNIDAD
# =========================================================
class Comunidad(models.Model):
    titulo = models.CharField(max_length=200)

    descripcion = models.TextField()

    imagen = models.ImageField(
        upload_to="comunidad/",
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    fecha_evento = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


# =========================================================
# PEDIDOS
# =========================================================
class Pedido(models.Model):

    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("en_camino", "En Camino"),
        ("entregado", "Entregado"),
    )

    cliente = models.CharField(max_length=150)

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    direccion = models.CharField(max_length=255)

    ciudad = models.CharField(max_length=120)

    repartidor_asignado = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_asignados'
    )

    fecha_pedido = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    entregado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

    def save(self, *args, **kwargs):

        if self.estado == "entregado":
            self.entregado = True
        else:
            self.entregado = False

        super().save(*args, **kwargs)


# =========================================================
# ENTREGAS
# =========================================================
class Entrega(models.Model):

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalle_entrega'
    )

    nombre_recibe = models.CharField(max_length=100)

    observacion = models.TextField(
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='entregas/',
        blank=True,
        null=True
    )

    foto_2 = models.ImageField(
        upload_to='entregas/',
        blank=True,
        null=True
    )

    firma = models.TextField(
        blank=True,
        null=True,
        help_text="Firma en Base64"
    )

    fecha = models.DateTimeField(auto_now_add=True)

    domiciliario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Entrega Pedido #{self.pedido.id}"


# =========================================================
# TESTIMONIOS
# =========================================================
class Testimonio(models.Model):

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Cliente"
    )

    comentario = models.TextField(
        max_length=300,
        verbose_name="Comentario"
    )

    fecha = models.DateTimeField(auto_now_add=True)

    activo = models.BooleanField(
        default=False,
        verbose_name="Aprobado"
    )

    destacado_inicio = models.BooleanField(
        default=False,
        verbose_name="Mostrar en inicio"
    )

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"

    def __str__(self):
        return f"{self.nombre} - {self.fecha.strftime('%d/%m/%Y')}"


# =========================================================
# INFORMACIÓN EMPRESA
# =========================================================
class InformacionEmpresa(models.Model):

    hero_titulo = models.CharField(
        max_length=200,
        verbose_name="Título Principal"
    )

    hero_descripcion = models.TextField(
        verbose_name="Descripción Principal"
    )

    hero_imagen = models.ImageField(
        upload_to='empresa/banner/',
        blank=True,
        null=True,
        verbose_name="Imagen Banner"
    )

    hero_video = models.FileField(
        upload_to='empresa/videos/',
        blank=True,
        null=True,
        verbose_name="Video Subido"
    )

    hero_video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL Video YouTube"
    )

    historia_titulo = models.CharField(
        max_length=200,
        verbose_name="Título Historia"
    )

    historia_descripcion = models.TextField(
        verbose_name="Descripción Historia"
    )

    historia_imagen = models.ImageField(
        upload_to='empresa/historia/',
        blank=True,
        null=True,
        verbose_name="Imagen Historia"
    )

    trabajo_titulo = models.CharField(
        max_length=200,
        verbose_name="Título Cómo Trabajamos"
    )

    trabajo_descripcion = models.TextField(
        verbose_name="Descripción Cómo Trabajamos"
    )

    trabajo_video = models.FileField(
        upload_to='empresa/trabajo/',
        blank=True,
        null=True,
        verbose_name="Video Trabajo"
    )

    trabajo_video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL Video Trabajo"
    )

    mision = models.TextField(
        verbose_name="Misión"
    )

    vision = models.TextField(
        verbose_name="Visión"
    )

    objetivo = models.TextField(
        verbose_name="Objetivo"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Información Empresa"
        verbose_name_plural = "Información Empresa"

    def __str__(self):
        return "Información Corporativa"


# =========================================================
# GALERÍA EMPRESA
# =========================================================
class GaleriaEmpresa(models.Model):

    titulo = models.CharField(
        max_length=200,
        blank=True
    )

    imagen = models.ImageField(
        upload_to='empresa/galeria/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='empresa/galeria/videos/',
        blank=True,
        null=True
    )

    video_url = models.URLField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(default=True)

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galería Empresa"
        verbose_name_plural = "Galería Empresa"

    def __str__(self):
        return self.titulo if self.titulo else f"Galería {self.id}"


# =========================================================
# SEÑALES
# =========================================================
@receiver(m2m_changed, sender=User.groups.through)
def asignar_staff_automatico(sender, instance, action, **kwargs):

    if action == "post_add":

        if instance.groups.filter(name="Domiciliarios").exists():
            instance.is_staff = True
            instance.save()