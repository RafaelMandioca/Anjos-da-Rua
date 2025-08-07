# core/views/animal.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from ..models import Animal, Especie
from ..forms.form_animal import AnimalForm, EspecieForm
from .cadastros_gerais import generic_create_update_view

# --- Animal Views ---
class AnimalListView(ListView): model = Animal
class AnimalDetailView(DetailView): model = Animal
class AnimalDeleteView(DeleteView): model = Animal; success_url = reverse_lazy('animal-list')

def animal_create(request):
    return generic_create_update_view(request, AnimalForm, 'Animal', 'core/generic_form.html', 'animal-list')

def animal_update(request, pk):
    return generic_create_update_view(request, AnimalForm, 'Animal', 'core/generic_form.html', 'animal-list', pk=pk)


# --- Especie Views ---
class EspecieListView(ListView): model = Especie
class EspecieDetailView(DetailView): model = Especie
class EspecieDeleteView(DeleteView): model = Especie; success_url = reverse_lazy('especie-list')

def especie_create(request):
    return generic_create_update_view(request, EspecieForm, 'Espécie', 'core/generic_form.html', 'especie-list')

def especie_update(request, pk):
    return generic_create_update_view(request, EspecieForm, 'Espécie', 'core/generic_form.html', 'especie-list', pk=pk)
