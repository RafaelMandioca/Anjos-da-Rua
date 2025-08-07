# core/forms/form_item.py

from django import forms
from ..models import Item

class ItemForm(forms.ModelForm):
    data_validade = forms.DateField(
        label="Data de Validade",
        widget=forms.TextInput(attrs={'class': 'date-mask', 'placeholder': 'DD/MM/AAAA'}),
        input_formats=['%d/%m/%Y', '%d/%m/%y']
    )

    class Meta:
        model = Item
        fields = ['nome', 'descricao', 'quantidade', 'preco_unitario', 'data_validade']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO AQUI: Formata o valor inicial da data para o padrão brasileiro
        if self.instance and self.instance.pk and self.instance.data_validade:
            self.initial['data_validade'] = self.instance.data_validade.strftime('%d/%m/%Y')