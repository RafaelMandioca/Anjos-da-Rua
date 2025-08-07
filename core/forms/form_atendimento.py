# core/forms/form_atendimento.py

from django import forms
from ..models import AtendimentoVeterinario, ItemHasAtendimentoVeterinario, TipoConsulta

class AtendimentoVeterinarioForm(forms.ModelForm):
    class Meta:
        model = AtendimentoVeterinario
        fields = ['animal', 'veterinario', 'tipo_consulta', 'data_do_atendimento', 'observacoes']
        widgets = {
            'data_do_atendimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TipoConsultaForm(forms.ModelForm):
    class Meta:
        model = TipoConsulta
        fields = ['descricao']

# Formset para adicionar Itens ao Atendimento
ItemAtendimentoFormSet = forms.inlineformset_factory(
    AtendimentoVeterinario,
    ItemHasAtendimentoVeterinario,
    fields=('item', 'quantidade'),
    extra=1,
    can_delete=True
)