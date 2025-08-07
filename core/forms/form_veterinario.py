# core/forms/form_veterinario.py

from django import forms
from ..models import Veterinario, CRMV

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        # O campo 'endereco' foi removido, pois será criado por outro formulário.
        fields = ['nome', 'cpf', 'email', 'telefone', 'senha_hash']
        widgets = {
            'senha_hash': forms.PasswordInput(),
        }

class CrmvForm(forms.ModelForm):
    class Meta:
        model = CRMV
        fields = ['numero', 'estado']