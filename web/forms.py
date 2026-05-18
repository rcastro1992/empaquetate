# En C:\...\empaquetate\web\forms.py

from django import forms
from .models import Testimonio

class FormularioContacto(forms.Form):
    # Campo para el nombre del usuario
    nombre = forms.CharField(
        label='Tu Nombre', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Completo'})
    )
    
    # Campo para el Asunto
    asunto = forms.CharField(
        label='Asunto', 
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'})
    )
    # Campo para el correo electrónico
    email = forms.EmailField(
        label='Tu Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    
    # Campo para el mensaje
    mensaje = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe aquí tu consulta...'}),
        max_length=500
    )

class TestimonioForm(forms.ModelForm):
    class Meta:
        model = Testimonio
        fields = ['nombre', 'comentario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Cuéntanos tu experiencia...', 'rows': 3}),
        }