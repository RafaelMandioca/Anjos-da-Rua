# core/forms.py

from django import forms
from .models import (
    Veterinario, CRMV, Endereco, Cidade, Abrigo, Especie, Animal,
    TipoConsulta, Item, AtendimentoVeterinario, ItemHasAtendimentoVeterinario
)

class VeterinarioForm(forms.ModelForm):
   class Meta:
      model = Veterinario
      fields = ['nome', 'cpf', 'email', 'telefone', 'senha_hash']
      widgets = {
         'senha_hash': forms.PasswordInput(),
      }

class CrmvForm(forms.ModelForm):
   class Meta:
      model = CRMV
      fields = ['numero', 'estado']

class EnderecoForm(forms.ModelForm):
   class Meta:
      model = Endereco
      fields = ['cep', 'bairro', 'logradouro', 'numero', 'complemento', 'ponto_de_referencia', 'cidade']

class CidadeForm(forms.ModelForm):
   class Meta:
      model = Cidade
      fields = '__all__'

class AbrigoForm(forms.ModelForm):
   class Meta:
      model = Abrigo
      fields = ['nome', 'endereco']

class EspecieForm(forms.ModelForm):
   class Meta:
      model = Especie
      fields = '__all__'

class AnimalForm(forms.ModelForm):
   class Meta:
      model = Animal
      fields = ['nome', 'especie', 'abrigo', 'peso', 'idade', 'sexo']

class TipoConsultaForm(forms.ModelForm):
   class Meta:
      model = TipoConsulta
      fields = ['descricao']

class ItemForm(forms.ModelForm):
   class Meta:
      model = Item
      fields = '__all__'
      widgets = {
         'data_validade': forms.DateInput(attrs={'type': 'date'}),
      }

class AtendimentoVeterinarioForm(forms.ModelForm):
   class Meta:
      model = AtendimentoVeterinario
      fields = ['animal', 'veterinario', 'tipo_consulta', 'data_do_atendimento', 'observacoes']
      widgets = {
         'data_do_atendimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
      }

# Formset para adicionar Itens ao Atendimento
ItemAtendimentoFormSet = forms.inlineformset_factory(
   AtendimentoVeterinario,
   ItemHasAtendimentoVeterinario,
   fields=('item', 'quantidade'),
   extra=1, # Começa com 1 formulário extra para adicionar um item
   can_delete=True # Permite remover itens
)