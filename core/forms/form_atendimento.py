# core/forms/form_atendimento.py

from django import forms
from django.forms import BaseInlineFormSet
from ..models import (
    AtendimentoVeterinario, ItemHasAtendimentoVeterinario, TipoConsulta, 
    Abrigo, Animal, Item
)

class AtendimentoVeterinarioForm(forms.ModelForm):
    data_do_atendimento = forms.DateTimeField(
        label="Data do Atendimento",
        widget=forms.TextInput(attrs={'class': 'datetime-mask', 'placeholder': 'DD/MM/AAAA HH:mm'}),
        input_formats=['%d/%m/%Y %H:%M', '%d/%m/%y %H:%M']
    )

    class Meta:
        model = AtendimentoVeterinario
        fields = ['animal', 'veterinario', 'tipo_consulta', 'data_do_atendimento', 'observacoes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['animal'].choices = self.get_animal_choices()
        
        # CORREÇÃO AQUI: Formata o valor inicial da data para o padrão brasileiro
        if self.instance and self.instance.pk and self.instance.data_do_atendimento:
            self.initial['data_do_atendimento'] = self.instance.data_do_atendimento.strftime('%d/%m/%Y %H:%M')

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

class ItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} (Estoque: {obj.quantidade})"

class ItemAtendimentoForm(forms.ModelForm):
    item = ItemChoiceField(queryset=Item.objects.filter(quantidade__gt=0).order_by('nome'))
    
    class Meta:
        model = ItemHasAtendimentoVeterinario
        fields = ['item', 'quantidade']

class BaseItemAtendimentoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        item_usage = {}
        for form in self.forms:
            if not form.is_valid() or form in self.deleted_forms:
                continue
            
            item = form.cleaned_data.get('item')
            quantidade = form.cleaned_data.get('quantidade')

            if item and quantidade:
                item_usage[item] = item_usage.get(item, 0) + quantidade
        
        for item, total_quantidade_usada in item_usage.items():
            if total_quantidade_usada > item.quantidade:
                raise forms.ValidationError(
                    f"Estoque insuficiente para o item '{item.nome}'. "
                    f"Solicitado: {total_quantidade_usada}, Disponível: {item.quantidade}."
                )

ItemAtendimentoFormSet = forms.inlineformset_factory(
    AtendimentoVeterinario,
    ItemHasAtendimentoVeterinario,
    form=ItemAtendimentoForm,
    formset=BaseItemAtendimentoFormSet,
    extra=1,
    can_delete=True
)