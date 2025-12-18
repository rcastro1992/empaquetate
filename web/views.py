# 
# ====== INICIO ========
# ======================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pedido, Entrega, Banner, Producto, Comunidad
from django.core.mail import send_mail, BadHeaderError

from .forms import FormularioContacto


# ======== PÚBLICO ================== 
# 
# 
def inicio(request):
    banners = Banner.objects.filter(activo=True)
    productos_mas_vendidos = Producto.objects.filter(mas_vendido=True)[:8]
    comunidad = Comunidad.objects.filter(activo=True)

    return render(request, 'inicio.html', {
        'banners': banners,
        'productos_mas_vendidos': productos_mas_vendidos,
        'comunidad': comunidad,
    })


def productos(request):
    # La query original está bien, solo corregimos el render.
    productos = Producto.objects.filter(unidades_disponibles__gt=0)
    
    # Se corrige la indentación excesiva del diccionario de contexto
    return render(request, "web/productos.html", {"productos": productos})


def detalle_producto(request, slug_producto):
    # Asegúrate de importar get_object_or_404 en la parte superior del archivo.
    # from django.shortcuts import get_object_or_404 
    producto = get_object_or_404(Producto, slug=slug_producto)
    
    return render(request, "web/producto_detalle.html", {"producto": producto})


def compania(request):
    return render(request, 'compania.html')


def contacto(request):
    formulario = FormularioContacto()
    mensaje_info = None
    
    if request.method == 'POST':
        formulario = FormularioContacto(request.POST)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            titulo = f"Nuevo mensaje de contacto - {datos['nombre']}"
            cuerpo = f"""
Has recibido un nuevo mensaje desde la web EMPAQUETATE:
Nombre: {datos['nombre']}
Correo: {datos['email']}
Mensaje:
{datos['mensaje']}
"""
            
            try:
                send_mail(
                    subject=titulo,
                    message=cuerpo,
                    from_email='contacto@empaquetate.com',
                    recipient_list=['contacto@empaquetate.com'],
                    fail_silently=False,
                )
                
                mensaje_info = "¡Tu mensaje se ha enviado correctamente!"
                formulario = FormularioContacto() # Limpiar formulario en caso de éxito
                
            except BadHeaderError:
                mensaje_info = "Error: Encabezado de correo inválido."
            except Exception as e:
                mensaje_info = f"Error al enviar el correo: {str(e)}"
            
            # 🛑 NO necesitas un 'return render' aquí. El render final lo maneja.
    
    # 🌟 ESTE ES EL RENDER FINAL. Se ejecuta si es GET, o POST (válido o inválido).
    return render(request, 'contacto.html', {
        'formulario': formulario,
        'mensaje_info': mensaje_info
    })

# ============================================================
# ==================  INTRANET / CONFIRMAR ENTREGA ===========
# ============================================================






@login_required
def intranet(request):
    """
    Vista para que el domiciliario confirme entregas:
    - Muestra pedidos pendientes
    - Permite registrar la entrega con evidencia
    """

    pedidos_pendientes = Pedido.objects.filter(entrega__isnull=True)

    # --- Si el usuario envía el formulario ---
    if request.method == "POST":
        pedido_id = request.POST.get("pedido")
        nombre_recibe = request.POST.get("nombre_recibe")
        observacion = request.POST.get("observacion")
        foto = request.FILES.get("foto")

        # Validar pedido pendiente
        try:
            pedido = Pedido.objects.get(id=pedido_id, entrega__isnull=True)
        except Pedido.DoesNotExist:
            return render(request, "confirmar_entrega.html", {
                "error": f"El pedido ID {pedido_id} no existe o ya fue entregado.",
                "pedidos": pedidos_pendientes
            })

        # Registrar entrega
        Entrega.objects.create(
            pedido=pedido,
            nombre_recibe=nombre_recibe,
            observacion=observacion,
            domiciliario=request.user,
            foto=foto
        )

        return render(request, "confirmar_entrega.html", {
            "mensaje": "Entrega registrada correctamente.",
            "pedidos": Pedido.objects.filter(entrega__isnull=True)
        })

    # --- Mostrar formulario inicial ---
    return render(request, "confirmar_entrega.html", {
        "pedidos": pedidos_pendientes
    })

# ============================================================
# ====================  LOGIN UNIFICADO  ======================
# ============================================================

from django.contrib.auth.views import LoginView
from django.urls import reverse

class UnifiedLoginView(LoginView):
    """
    Un solo login para todos los tipos de usuarios.
    Admin → dashboard admin
    Usuarios normales → intranet (confirmar entrega)
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        # Si es administrador o staff → panel admin
        if user.is_staff or user.is_superuser:
            return reverse('admin:index')

        # Usuario normal → intranet (confirmar entrega)
        return reverse('intranet')

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')

        # Sesión expira al cerrar navegador si NO marcó "recordar sesión"
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30 días

        return super().form_valid(form)
