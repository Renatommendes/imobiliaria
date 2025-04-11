from django import forms
from .models import Cliente
from django.contrib.auth.models import User
from .models import Contrato
from .models import OrdemContrato, EtapaContrato
from .models import FaseProcesso
from .models import ItemFaseProcesso


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'email', 'telefone', 'endereco']


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso. Escolha outro.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "As senhas não coincidem.")

        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_superuser']


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['usuario', 'nome', 'tipo', 'arquivo']




class OrdemContratoForm(forms.ModelForm):
    nova_etapa = forms.CharField(
        required=False, 
        label="Nova Etapa", 
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nome da etapa'})
    )

    class Meta:
        model = OrdemContrato
        fields = ['usuario', 'nome', 'tipo', 'tipo_envio', 'arquivo', 'status', 'nova_etapa']

    def clean(self):
        cleaned_data = super().clean()
        nova_etapa = cleaned_data.get('nova_etapa')
        usuario = cleaned_data.get('usuario')

        if nova_etapa and usuario:
            etapa_existente = EtapaContrato.objects.filter(numero=nova_etapa, usuario=usuario).first()
            if not etapa_existente:
                etapa_existente = EtapaContrato.objects.create(numero=nova_etapa, usuario=usuario)

            cleaned_data['etapa'] = etapa_existente

        return cleaned_data



class UploadContratoForm(forms.ModelForm):
    class Meta:
        model = OrdemContrato
        fields = ['arquivo']
        labels = {'arquivo': 'Atualizar Contrato (PDF)'}

        

class EditarArquivoForm(forms.ModelForm):
    class Meta:
        model = OrdemContrato
        fields = ["arquivo"]  # 🔹 Permite apenas a edição do arquivo



class FaseProcessoForm(forms.ModelForm):
    class Meta:
        model = FaseProcesso
        fields = ['usuario', 'numero', 'nome']
        labels = {
                        'usuario': 'Usuário',
                        'numero': 'Número da Fase',
                        'nome': 'Nome da Fase',
                    }
        
class ItemFaseProcessoForm(forms.ModelForm):
    class Meta:
        model = ItemFaseProcesso
        fields = [ 'titulo', 'descricao', 'arquivo']