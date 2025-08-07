# core/forms/form_veterinario.py

from django import forms
from ..models import Veterinario, CRMV

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone']

class CrmvForm(forms.ModelForm):
    class Meta:
        model = CRMV
        fields = ['numero', 'estado']