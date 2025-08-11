# core/forms.py

from django import forms
from .models import (
    Veterinario, CRMV, Endereco, Cidade, Abrigo, Especie, Animal,
    TipoConsulta, Item, AtendimentoVeterinario, ItemHasAtendimentoVeterinario, CodigoAcesso
)

# --- Formulários de Registro ---

class VeterinarioRegistrationForm(forms.ModelForm):
    codigo_acesso = forms.CharField(max_length=36, required=True, help_text="Insira o código de acesso fornecido pelo administrador.")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone']

    def clean_codigo_acesso(self):
        codigo = self.cleaned_data.get('codigo_acesso')
        try:
            if not CodigoAcesso.objects.filter(codigo=codigo, utilizado=False).exists():
                raise forms.ValidationError("Código de acesso inválido ou já utilizado.")
        except:
             raise forms.ValidationError("Código de acesso inválido ou já utilizado.")
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")
    
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        return user

# --- Outros Formulários ---

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['nome', 'cpf', 'email', 'telefone']

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
        fields = ['nome']

class EspecieForm(forms.ModelForm):
   class Meta:
      model = Especie
      fields = '__all__'

class AnimalForm(forms.ModelForm):
   class Meta:
      model = Animal
      fields = ['nome', 'abrigo', 'peso', 'idade', 'sexo']

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
    abrigo = forms.ModelChoiceField(queryset=Abrigo.objects.all(), required=False)

    class Meta:
        model = AtendimentoVeterinario
        fields = ['abrigo', 'animal', 'veterinario', 'tipo_consulta', 'data_do_atendimento', 'observacoes']
        widgets = {
            'data_do_atendimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animal'].queryset = Animal.objects.none()

        if 'abrigo' in self.data:
            try:
                abrigo_id = int(self.data.get('abrigo'))
                self.fields['animal'].queryset = Animal.objects.filter(abrigo_id=abrigo_id).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.animal:
            self.fields['animal'].queryset = Animal.objects.filter(abrigo=self.instance.animal.abrigo).order_by('nome')


ItemAtendimentoFormSet = forms.inlineformset_factory(
   AtendimentoVeterinario,
   ItemHasAtendimentoVeterinario,
   fields=('item', 'quantidade'),
   extra=1,
   can_delete=True
)