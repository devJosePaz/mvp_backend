from django.db import models
from django.contrib.auth.models import User
import json

class PreferenciasUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.CharField(max_length=20)
    nivel = models.CharField(max_length=20)
    horas = models.FloatField()
    criado_em = models.DateTimeField(auto_now_add=True)
    recomendacoes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.materia} ({self.nivel})"