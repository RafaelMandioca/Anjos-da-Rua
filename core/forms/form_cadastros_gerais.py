# core/forms/form_cadastros_gerais.py

from django import forms
from ..models import Cidade, Endereco, Abrigo

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = '__all__'

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'bairro', 'logradouro', 'numero', 'complemento', 'ponto_de_referencia', 'cidade']

class AbrigoForm(forms.ModelForm):
    class Meta:
        model = Abrigo
        fields = ['nome', 'endereco']