# core/forms/form_veterinario.py

from django import forms
from ..models import Veterinario, CRMV

class VeterinarioForm(forms.ModelForm):
    """
    Formulário para a criação de um Veterinário por um administrador.
    """
    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone']

class VeterinarioUpdateForm(forms.ModelForm):
    """
    Formulário para o próprio usuário veterinário atualizar suas informações básicas.
    """
    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone']

class CrmvForm(forms.ModelForm):
    """
    Formulário para criar ou editar um registro de CRMV.
    """
    class Meta:
        model = CRMV
        fields = ['numero', 'estado']
