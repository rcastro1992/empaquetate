from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



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


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    referencia = models.CharField(max_length=50, blank=True, null=True)
    colores = models.CharField(max_length=200, blank=True, null=True)
    medidas = models.CharField(max_length=200, blank=True, null=True)
    mas_vendido = models.BooleanField(default=False)


    unidades_disponibles = models.PositiveIntegerField(default=0, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    @property
    def colores_lista(self):
        """Devuelve la lista de colores separada por comas."""
        if self.colores:
            return [c.strip() for c in self.colores.split(",") if c.strip()]
        return []

class Comunidad(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="comunidad/", blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_evento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo



class Pedido(models.Model):
    cliente = models.CharField(max_length=100)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"


class Entrega(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    nombre_recibe = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='entregas/', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    domiciliario = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Entrega Pedido #{self.pedido.id} - Recibe: {self.nombre_recibe}"



