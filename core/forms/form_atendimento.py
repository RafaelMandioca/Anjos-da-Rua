# core/forms/form_atendimento.py

from django import forms
from django.forms import BaseInlineFormSet
from ..models import (
    AtendimentoVeterinario, ItemHasAtendimentoVeterinario, TipoConsulta, 
    Abrigo, Animal, Item, StatusAtendimento
)

class AtendimentoVeterinarioForm(forms.ModelForm):
    data_do_atendimento = forms.DateTimeField(
        label="Data do Atendimento",
        widget=forms.TextInput(attrs={'class': 'datetime-mask', 'placeholder': 'DD/MM/AAAA HH:mm'}),
        input_formats=['%d/%m/%Y %H:%M', '%d/%m/%y %H:%M']
    )

    class Meta:
        model = AtendimentoVeterinario
        fields = ['animal', 'veterinario', 'tipo_consulta', 'status', 'data_do_atendimento', 'observacoes']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        initial_animal = kwargs.pop('initial_animal', None)
        super().__init__(*args, **kwargs)

        is_editing = self.instance and self.instance.pk
        is_admin = user and user.is_superuser

        if is_editing:
            if not is_admin:
                self.fields['animal'].disabled = True
                self.fields['animal'].required = False
            else:
                self.fields['animal'].choices = self.get_animal_choices()
        else:
            if initial_animal:
                self.fields['animal'].queryset = Animal.objects.filter(pk=initial_animal.pk)
                self.initial['animal'] = initial_animal
                self.fields['animal'].disabled = True
            else:
                if is_admin:
                    self.fields['animal'].choices = self.get_animal_choices()
                else:
                    self.fields['animal'].queryset = Animal.objects.none()
                    self.fields['animal'].disabled = True
        
        is_concluido = is_editing and self.instance.status and self.instance.status.descricao == 'Concluído'
        if is_concluido:
            for field_name, field in self.fields.items():
                if field_name != 'status':
                    field.disabled = True
        
        if is_editing and self.instance.data_do_atendimento:
            self.initial['data_do_atendimento'] = self.instance.data_do_atendimento.strftime('%d/%m/%Y %H:%M')

    def get_animal_choices(self):
        choices = [('', '---------')]
        abrigos = Abrigo.objects.prefetch_related('animal_set').order_by('nome')
        for abrigo in abrigos:
            animais_do_abrigo = [(animal.pk, animal.nome) for animal in abrigo.animal_set.all()]
            if animais_do_abrigo:
                choices.append((abrigo.nome, animais_do_abrigo))
        return choices
        
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if self.instance and self.instance.pk and self.instance.status:
            if self.instance.status.descricao == 'Concluído' and status.descricao != 'Concluído':
                raise forms.ValidationError("Um atendimento concluído não pode ser alterado para 'Não Concluído'.")
        return status

class VeterinarioAtendimentoForm(AtendimentoVeterinarioForm):
    class Meta(AtendimentoVeterinarioForm.Meta):
        fields = ['animal', 'tipo_consulta', 'status', 'data_do_atendimento', 'observacoes']


class TipoConsultaForm(forms.ModelForm):
    class Meta:
        model = TipoConsulta
        fields = ['descricao']

class ItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} (Estoque: {obj.quantidade})"

class ItemAtendimentoForm(forms.ModelForm):
    item = ItemChoiceField(queryset=Item.objects.none(), required=False)
    quantidade = forms.IntegerField(min_value=1)
    
    class Meta:
        model = ItemHasAtendimentoVeterinario
        fields = ['item', 'quantidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        current_item = self.instance.item if self.instance and self.instance.pk else None
        
        items_in_stock = Item.objects.filter(quantidade__gt=0)
        
        if current_item:
            self.fields['item'].queryset = (items_in_stock | Item.objects.filter(pk=current_item.pk)).distinct().order_by('nome')
        else:
            self.fields['item'].queryset = items_in_stock.order_by('nome')

class BaseItemAtendimentoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        is_concluido = self.instance and self.instance.pk and self.instance.status and self.instance.status.descricao == 'Concluído'
        if is_concluido:
            return

        for form in self.forms:
            if not form.is_valid() or self.can_delete and self._should_delete_form(form):
                continue
            
            item = form.cleaned_data.get('item')
            quantidade_solicitada = form.cleaned_data.get('quantidade')

            if item and quantidade_solicitada:
                if quantidade_solicitada > item.quantidade:
                    form.add_error('quantidade', f"Estoque insuficiente para '{item.nome}'. Disponível: {item.quantidade}.")

ItemAtendimentoFormSet = forms.inlineformset_factory(
    AtendimentoVeterinario,
    ItemHasAtendimentoVeterinario,
    form=ItemAtendimentoForm,
    formset=BaseItemAtendimentoFormSet,
    extra=1,
    can_delete=True
)