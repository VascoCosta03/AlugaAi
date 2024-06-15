from django.db import models

# Create your models here.

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=255)
    foto_url = models.CharField(max_length=255, default='null')

    def __str__(self):
        return self.categoria
    
class Localizacao(models.Model):
    id_localizacao = models.AutoField(primary_key=True)
    localizacao = models.CharField(max_length=255)

    def __str__(self):
        return self.localizacao
    
class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    foto_url = models.CharField(max_length=255, default='null')
    saldo = models.FloatField()

    def __str__(self):
        return self.nome
    
class Anuncio(models.Model):
    ESTADO_CHOICES = (
        ("Novo", "Novo"),
        ("Semi-novo", "Semi-novo"),
        ("Usado", "Usado"),
    )
    
    id_anuncio = models.AutoField(primary_key=True)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    preco = models.FloatField()
    foto_url = models.CharField(max_length=255, default='null')
    ativo = models.BooleanField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    descricao = models.TextField(default='null')

    def __str__(self):
        return self.nome