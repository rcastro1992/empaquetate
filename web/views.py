from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Pedido, Entrega, Banner
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from .forms import FormularioContacto

# ✅ SOLUCIÓN: Importación correcta del formulario desde la misma app
from .forms import FormularioContacto 


# --- VISTAS PÚBLICAS ---

def inicio(request):
    banners = Banner.objects.filter(activo=True)
    productos_mas_vendidos = Producto.objects.filter(mas_vendido=True)[:8]

    return render(request, 'inicio.html', {
        'banners': banners,
        'productos_mas_vendidos': productos_mas_vendidos,
    })



def productos(request):
    productos = Producto.objects.filter(unidades_disponibles__gt=0)
    return render(request, "web/productos.html", {"productos": productos})

def detalle_producto(request, slug_producto):
    producto = get_object_or_404(Producto, slug=slug_producto)
    return render(request, "web/producto_detalle.html", {"producto": producto})

from .models import Producto, Banner, Comunidad

def inicio(request):
    banners = Banner.objects.filter(activo=True)
    productos_mas_vendidos = Producto.objects.filter(mas_vendido=True)[:8]
    comunidad = Comunidad.objects.filter(activo=True)

    return render(request, 'inicio.html', {
        'banners': banners,
        'productos_mas_vendidos': productos_mas_vendidos,
        'comunidad': comunidad,
    })




def compania(request):
    return render(request, 'compania.html')


def contacto(request):
    # ... (El código de contacto ahora funciona porque FormularioContacto está importado) ...
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
                # Reinstancia el formulario para que aparezca limpio
                formulario = FormularioContacto() 
            except BadHeaderError:
                mensaje_info = "Error: Encabezado de correo inválido."
            except Exception as e:
                mensaje_info = f"Error al enviar el correo: {str(e)}"

    return render(request, 'contacto.html', {
        'formulario': formulario,
        'mensaje_info': mensaje_info
    })



# --- VISTA PRIVADA (INTRANET) ---

@login_required
def intranet(request):

    if request.method == "POST":

        pedido_id = request.POST.get("pedido")
        nombre_recibe = request.POST.get("nombre_recibe")
        observacion = request.POST.get("observacion")
        foto = request.FILES.get("foto")

        # Obtener pedido
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            pedidos_pendientes = Pedido.objects.filter(entregado=False)
            return render(request, "confirmar_entrega.html", {
                "error": f"El pedido ID {pedido_id} no existe o ya fue entregado.",
                "pedidos": pedidos_pendientes
            })

        # Crear entrega
        entrega = Entrega(
            pedido=pedido,
            nombre_recibe=nombre_recibe,
            observacion=observacion,
            domiciliario=request.user
        )

        if foto:
            entrega.foto = foto

        entrega.save()

        # ✅ CORRECCIÓN CRÍTICA: Marcar el pedido como entregado
        pedido.entregado = True
        pedido.save()
        
        # Redireccionar para evitar re-envío de formulario
        return redirect('intranet') 

    # GET: Muestra solo pedidos pendientes
    pedidos_pendientes = Pedido.objects.filter(entregado=False) 
    return render(request, "confirmar_entrega.html", {
        "pedidos": pedidos_pendientes
    })
