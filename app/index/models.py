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
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, default=1)  # Adicione um valor padrão temporário
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, default='Título do Anúncio')
    preco = models.FloatField()
    foto_url = models.CharField(max_length=255, default='null')
    ativo = models.BooleanField(default=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="Novo")
    descricao = models.TextField()

    def __str__(self):
        return self.titulo
    
    def get_anuncio_count(self):
        return Anuncio.objects.filter(utilizador=self).count()
        
    def get_favorite_count(self):
        return Favorito.objects.filter(anuncio=self).count()
    
    def get_aluguer_count(self):
        return ProdutoAlugado.objects.filter(anuncio=self).count()
    
class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_favorito
    
class ProdutoAlugado(models.Model):
    
    id_produto_alugado = models.AutoField(primary_key=True)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    preco_total = models.FloatField()

    def __str__(self):
        return self.anuncio.titulo
    
class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    utilizador1 = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='chats_started')  # New related_name
    utilizador2 = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='chats_participating')  # New related_name



    def __str__(self):
        return self.id_chat
    
class Mensagem(models.Model):
    id_mensagem = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    remetente = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data = models.DateTimeField()

    def __str__(self):
        return self.mensagem