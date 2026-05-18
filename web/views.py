from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.urls import reverse

from .forms import FormularioContacto, TestimonioForm

from .models import (
    Pedido,
    Entrega,
    Banner,
    Producto,
    Comunidad,
    Testimonio,
    InformacionEmpresa,
    GaleriaEmpresa
)

# ======== PÚBLICO ================== 

def inicio(request):
    """
    Vista de inicio: 
    1. Carga banners, productos y testimonios aprobados.
    2. Procesa el formulario de nuevos comentarios de clientes.
    """
    banners = Banner.objects.filter(activo=True)
    productos_mas_vendidos = Producto.objects.filter(mas_vendido=True)[:8]
    
    # Solo mostramos testimonios que tú ya aprobaste (activo=True)
    testimonios = Testimonio.objects.filter(activo=True, destacado_inicio=True).order_by('-fecha')
    comunidad = Comunidad.objects.filter(activo=True)

    # Lógica para recibir comentarios de clientes
    if request.method == 'POST' and 'btn_testimonio' in request.POST:
        form_testimonio = TestimonioForm(request.POST)
        if form_testimonio.is_valid():
            # Se guarda con activo=False por defecto (según el modelo)
            form_testimonio.save()
            return redirect('inicio')
    else:
        form_testimonio = TestimonioForm()

    return render(request, 'inicio.html', {
        'banners': banners,
        'productos_mas_vendidos': productos_mas_vendidos,
        'testimonios': testimonios,
        'comunidad': comunidad,
        'form_testimonio': form_testimonio,
    })

def productos(request):
    productos = Producto.objects.filter(unidades_disponibles__gt=0)
    return render(request, "web/productos.html", {"productos": productos})

def detalle_producto(request, slug_producto):
    producto = get_object_or_404(Producto, slug=slug_producto)
    return render(request, "web/producto_detalle.html", {"producto": producto})

def compania(request):

    info = InformacionEmpresa.objects.filter(activo=True).first()

    galeria = GaleriaEmpresa.objects.filter(activo=True)

    return render(request,
                  'compania.html',
                  {
                      'info': info,
                      'galeria': galeria
                  })

def contacto(request):
    formulario = FormularioContacto()
    mensaje_info = None
    
    if request.method == 'POST':
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            titulo = f"Nuevo mensaje de contacto - {datos['nombre']}"
            cuerpo = f"Nombre: {datos['nombre']}\nCorreo: {datos['email']}\nMensaje:\n{datos['mensaje']}"
            
            try:
                send_mail(
                    subject=titulo,
                    message=cuerpo,
                    from_email='contacto@empaquetate.com',
                    recipient_list=['contacto@empaquetate.com'],
                    fail_silently=False,
                )
                mensaje_info = "¡Tu mensaje se ha enviado correctamente!"
                formulario = FormularioContacto()
            except Exception as e:
                mensaje_info = f"Error al enviar el correo: {str(e)}"
    
    return render(request, 'contacto.html', {'formulario': formulario, 'mensaje_info': mensaje_info})

# ============================================================
# ==================  INTRANET / APP DOMICILIARIO  ===========
# ============================================================

@login_required
def intranet(request):
    pedidos_pendientes = Pedido.objects.filter(
        repartidor_asignado=request.user, 
        estado='en_camino'
    ).order_by('-fecha_pedido')

    return render(request, "intranet.html", {
        "pedidos": pedidos_pendientes
    })

@login_required
def completar_entrega(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, repartidor_asignado=request.user)

    if request.method == "POST":
        nombre_recibe = request.POST.get("nombre_recibe")
        observacion = request.POST.get("observacion")
        foto = request.FILES.get("foto")
        foto_2 = request.FILES.get("foto_2")
        firma_data = request.POST.get("firma") 

        Entrega.objects.create(
            pedido=pedido,
            nombre_recibe=nombre_recibe,
            observacion=observacion,
            foto=foto,
            foto_2=foto_2,
            firma=firma_data,
            domiciliario=request.user
        )

        pedido.estado = 'entregado'
        pedido.save()

        return redirect('intranet')

    return render(request, "completar_entrega.html", {"pedido": pedido})

# ============================================================
# ====================  LOGIN UNIFICADO  ======================
# ============================================================

class UnifiedLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse('admin:index')
        return reverse('intranet')

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30) # 30 días
        return super().form_valid(form)
    
    # COMENTARIOS CLIENTES
def dejar_comentario(request):
    if request.method == 'POST':
        form = TestimonioForm(request.POST)
        if form.is_valid():
            form.save() # Se guarda como inactivo por defecto
            return render(request, 'comentario_exitoso.html') # Una paginita de gracias
    else:
        form = TestimonioForm()
    
    return render(request, 'dejar_comentario.html', {'form': form})