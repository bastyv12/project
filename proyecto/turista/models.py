from django.db import models

from django.db import models
from django.contrib.auth.models import User

CATEGORIAS = [
    ('playa', 'Playa'),
    ('parque', 'Parque'),
    ('museo', 'Museo'),
    ('montaña', 'Montaña'),
    ('ciudad', 'Ciudad'),
]

class LugarTuristico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='lugares/')
    horario = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='ciudad')

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    lugar = models.ForeignKey(LugarTuristico, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=500)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.lugar.nombre}'

# 🔥 Agenda personalizada de usuario
class AgendaViajes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    lugar = models.ForeignKey(LugarTuristico, on_delete=models.CASCADE)
    fecha_planificada = models.DateField()
    es_favorito = models.BooleanField(default=False)
    notas = models.TextField(blank=True)

    class Meta:
        unique_together = ('usuario', 'lugar')  # Evita duplicados

    def __str__(self):
        return f'{self.usuario.username} - {self.lugar.nombre}'
