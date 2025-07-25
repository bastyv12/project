from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LugarTuristico, Comentario
from django.contrib.auth.models import User
from django.db import models
from .models import AgendaViajes


# Formulario para registrar lugares
class LugarForm(forms.ModelForm):
    class Meta:
        model = LugarTuristico
        fields = ['nombre', 'descripcion', 'ubicacion', 'horario', 'imagen', 'categoria']

# Formulario para comentar
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'calificacion']

# Formulario personalizado de registro de usuario
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

class AgendaForm(forms.ModelForm):
    class Meta:
        model = AgendaViajes
        fields = ['fecha_planificada', 'notas']
        widgets = {
            'fecha_planificada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }