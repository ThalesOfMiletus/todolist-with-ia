# models.py
from django.db import models

class Task(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
