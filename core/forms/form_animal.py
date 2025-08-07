# core/forms/form_animal.py

from django import forms
from ..models import Animal, Especie

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'abrigo', 'peso', 'idade', 'sexo']

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = '__all__'
