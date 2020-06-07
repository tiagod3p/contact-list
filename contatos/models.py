from django.db import models
from django.utils import timezone

"""
CONTATOS
id: INT (automático)  -> Não precisa colocar na classe
nome: STR * (obrigatório) -> STR = charfield
sobrenome: STR (opcional) -> Opcionais, setar: blank=True
telefone: STR * (obrigatório)
email: STR (opcional)
data_criacao: DATETIME (automático) -> DateTimeField timezone.now
descricao: texto -> texto = textfield
categoria: CATEGORIA (outro model) -> ForeignKey

 CATEGORIA
 id: INT - > Não precisa colocar na classe
 nome: STR * (obrigatório)

"""


class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d')

    def __str__(self):
        return self.nome
