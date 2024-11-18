from django.db import models

# Create your models here.

class Alunos(models.Model):
    #remover linha
    imagem = models.FileField(upload_to='imagem_alunos', null=True, blank=False)
    serie = models.CharField(max_length=50)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    #eletiva que ele estuda #remover linha
    eletiva = models.CharField(max_length=50, null=True, blank=False)

class Professores(models.Model):
    #eletiva que ele ensina
    eletiva = models.CharField(max_length=100,null=True, blank=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    idade = models.IntegerField()
    graduacao = models.CharField(max_length=100,null=True, blank=False)
    #remover linha
    imagem = models.FileField(upload_to='imagem_professores', null=True, blank=False)
    #remover linha
    professor = models.BooleanField(null=True, blank=False)
    #remover linha
    tutor = models.BooleanField(null=True, blank=False)
    #remover linha
    descricao = models.CharField(max_length=1000,null=True, blank=False)

class Admins(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)
    #retirar o null e o blank daqui
    acoes = models.CharField(max_length=100,null=True, blank=False)
    #remover linha
    imagem = models.FileField(upload_to='imagem_admins', null=True, blank=False)

class Eletivas(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=150)
    imagem = models.ImageField(upload_to="img_eletivas/")
    #remover linha
    link = models.URLField(max_length=100, null=True, blank=False)
    #remover linha
    img_professores_eletiva = models.ImageField(upload_to="img_eletivas/img_professores_eletiva",null=True, blank=False)


class Anuncio(models.Model):
    titulo = models.CharField(max_length=40)
    descricao = models.TextField(max_length=73)
    imagem = models.ImageField(upload_to="img_anuncio/")
    #remover linha
    link = models.URLField(max_length=100, null=True, blank=False)

#14 alunos pra cada eletiva
class PaginasUtilizaveis(models.Model):
    tutoria = models.BooleanField()
    eletiva = models.BooleanField()
    index = models.BooleanField()
    sobre = models.BooleanField(null=True, blank=False)

class OqueTemosaOferecer(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=76)
    imagem = models.ImageField(upload_to="img_OqueTemosaOferecer/")
    #remover linha
    link = models.URLField(max_length=200)
    titulo_do_link = models.CharField(max_length=100)

class CarrosselProfessores(models.Model):
    ids = models.TextField(max_length=2000)
    
    