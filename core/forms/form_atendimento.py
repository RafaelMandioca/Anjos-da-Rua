# core/forms/form_atendimento.py

from django import forms
from django.forms import BaseInlineFormSet
from ..models import (
    AtendimentoVeterinario, ItemHasAtendimentoVeterinario, TipoConsulta, 
    Abrigo, Animal, Item
)

# --- Formulário de Atendimento Principal ---

class AtendimentoVeterinarioForm(forms.ModelForm):
    class Meta:
        model = AtendimentoVeterinario
        fields = ['animal', 'veterinario', 'tipo_consulta', 'data_do_atendimento', 'observacoes']
        widgets = {
            'data_do_atendimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animal'].choices = self.get_animal_choices()

    def get_animal_choices(self):
        choices = [('', '---------')]
        abrigos = Abrigo.objects.prefetch_related('animal_set').order_by('nome')
        for abrigo in abrigos:
            animais_do_abrigo = [(animal.pk, animal.nome) for animal in abrigo.animal_set.all()]
            if animais_do_abrigo:
                choices.append((abrigo.nome, animais_do_abrigo))
        return choices

class VeterinarioAtendimentoForm(AtendimentoVeterinarioForm):
    class Meta(AtendimentoVeterinarioForm.Meta):
        fields = ['animal', 'tipo_consulta', 'data_do_atendimento', 'observacoes']


class TipoConsultaForm(forms.ModelForm):
    class Meta:
        model = TipoConsulta
        fields = ['descricao']


# --- Formulários de Itens com Validação de Estoque ---

# 1. Campo de Seleção Customizado para mostrar o estoque
class ItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} (Estoque: {obj.quantidade})"

# 2. Formulário para cada linha de item, usando o campo customizado
class ItemAtendimentoForm(forms.ModelForm):
    item = ItemChoiceField(queryset=Item.objects.filter(quantidade__gt=0).order_by('nome'))
    
    class Meta:
        model = ItemHasAtendimentoVeterinario
        fields = ['item', 'quantidade']

# 3. FormSet Base com a lógica de validação de estoque
class BaseItemAtendimentoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        # Dicionário para rastrear o uso total de cada item neste formulário
        item_usage = {}

        for form in self.forms:
            if not form.is_valid() or form in self.deleted_forms:
                continue
            
            item = form.cleaned_data.get('item')
            quantidade = form.cleaned_data.get('quantidade')

            if item and quantidade:
                # Acumula a quantidade usada para cada item
                item_usage[item] = item_usage.get(item, 0) + quantidade
        
        # Valida o uso total de cada item contra o estoque disponível
        for item, total_quantidade_usada in item_usage.items():
            if total_quantidade_usada > item.quantidade:
                # Adiciona um erro geral ao formset
                raise forms.ValidationError(
                    f"Estoque insuficiente para o item '{item.nome}'. "
                    f"Solicitado: {total_quantidade_usada}, Disponível: {item.quantidade}."
                )

# 4. Factory que une o FormSet Base com o Formulário de Item
ItemAtendimentoFormSet = forms.inlineformset_factory(
    AtendimentoVeterinario,
    ItemHasAtendimentoVeterinario,
    form=ItemAtendimentoForm,       # Usa nosso formulário customizado
    formset=BaseItemAtendimentoFormSet, # Usa nossa classe de validação
    extra=1,
    can_delete=True
)