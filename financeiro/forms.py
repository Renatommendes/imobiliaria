from django import forms
from .models import Boleto
from datetime import datetime, date  # Importando date corretamente

class BoletoForm(forms.ModelForm):
    class Meta:
        model = Boleto
        fields = ['usuario', 'valor', 'data_vencimento', 'pago', 'arquivo_pdf']

    def clean_data_vencimento(self):
        data = self.cleaned_data.get('data_vencimento')

        # Aqui corrigimos a referência para date
        if isinstance(data, date):  # Agora está correto
            return data

        # Se for string, faz a conversão correta
        try:
            return datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            raise forms.ValidationError("Formato de data inválido. Use dd/mm/yyyy.")
