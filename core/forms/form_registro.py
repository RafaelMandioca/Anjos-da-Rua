# core/forms/form_registro.py

from django import forms
from ..models import Veterinario, CodigoAcesso

class VeterinarioRegistrationForm(forms.ModelForm):
    codigo_acesso = forms.CharField(max_length=36, required=True, help_text="Insira o código de acesso fornecido pelo administrador.")
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone', 'senha']

    def clean_codigo_acesso(self):
        codigo = self.cleaned_data.get('codigo_acesso')
        if not CodigoAcesso.objects.filter(codigo=codigo, utilizado=False).exists():
            raise forms.ValidationError("Código de acesso inválido ou já utilizado.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")

    def save(self, commit=True):
        veterinario = super().save(commit=False)
        veterinario.set_password(self.cleaned_data["senha"])
        if commit:
            veterinario.save()
            codigo_acesso = CodigoAcesso.objects.get(codigo=self.cleaned_data.get('codigo_acesso'))
            codigo_acesso.utilizado = True
            codigo_acesso.save()
        return veterinario