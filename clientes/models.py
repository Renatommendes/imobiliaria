from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relaciona com User
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()

    def __str__(self):
        return self.nome





class Contrato(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=255, default="Contrato Padrão")
    tipo = models.CharField(max_length=20, choices=[('venda', 'Venda'), ('locacao', 'Locação')])
    arquivo = models.FileField(upload_to='contratos/', null=True, blank=True)  # Permite valores nulos
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)


class EtapaContrato(models.Model):
    numero = models.CharField(max_length=255)  # 🔹 Removido o unique=True
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habilitada = models.BooleanField(default=False)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.numero

    class Meta:
        unique_together = ('numero', 'usuario')  # 🔥 Garante que o mesmo número só pode existir uma vez por usuário
 


class OrdemContrato(models.Model):
    TIPO_ENVIO_CHOICES = [
        ('envio', 'Envio pelo Usuário'),
        ('visualizacao', 'Somente Visualização'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    etapa = models.ForeignKey('EtapaContrato', on_delete=models.CASCADE, related_name="ordens")
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    tipo_envio = models.CharField(  # 🔹 Novo campo adicionado
        max_length=20,
        choices=TIPO_ENVIO_CHOICES,
        default='envio',
        verbose_name='Tipo de Envio'
    )
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
    ])
    data_criacao = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='contratos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.status}"



class FaseProcesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"Fase {self.numero} - {self.nome}"
    
class ItemFaseProcesso(models.Model):
    fase = models.ForeignKey(FaseProcesso, on_delete=models.CASCADE, related_name="itens")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='itens_fase/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.fase.nome}"