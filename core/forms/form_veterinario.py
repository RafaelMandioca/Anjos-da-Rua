# core/forms/form_veterinario.py

from django import forms
from ..models import Veterinario, CRMV

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        # O campo 'endereco' será selecionado, não criado aqui.
        fields = ['nome', 'cpf', 'email', 'telefone', 'senha_hash', 'endereco']
        widgets = {
            'senha_hash': forms.PasswordInput(),
        }

class CrmvForm(forms.ModelForm):
    class Meta:
        model = CRMV
        fields = ['numero', 'estado']
