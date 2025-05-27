from django.db import models
from django.contrib.auth.models import User

class PreferenciasUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.CharField(max_length=20)
    nivel = models.CharField(max_length=20)
    horas_por_semana = models.IntegerField()  #
    criado_em = models.DateTimeField(auto_now_add=True)