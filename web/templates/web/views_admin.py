from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Producto


# Solo administradores pueden usar esta vista
@user_passes_test(lambda u: u.is_staff)
def toggle_mas_vendido(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        producto.mas_vendido = not producto.mas_vendido
        producto.save()
        return JsonResponse({"ok": True, "mas_vendido": producto.mas_vendido})
    except Producto.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Producto no encontrado"})
