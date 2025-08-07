# core/forms/form_item.py

from django import forms
from ..models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'data_validade': forms.DateInput(attrs={'type': 'date'}),
        }
