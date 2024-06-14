from django.db import models

# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=255)
    foto_url = models.CharField(max_length=255, default='null')

    def __str__(self):
        return self.categoria