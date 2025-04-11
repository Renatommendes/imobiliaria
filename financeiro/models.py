from django.db import models
from django.contrib.auth.models import User

class Boleto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Agora o boleto pertence a um usuário
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    arquivo_pdf = models.FileField(upload_to='boletos/', blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.data_vencimento.strftime('%d/%m/%Y')}"
