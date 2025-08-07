# core/views/animal.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from ..models import Animal, Especie
from ..forms.form_animal import AnimalForm, EspecieForm
from .cadastros_gerais import generic_create_update_view

# --- Animal Views ---
class AnimalListView(ListView): 
    model = Animal
    template_name = 'core/animal/animal_list.html'

class AnimalDetailView(DetailView): 
    model = Animal
    template_name = 'core/animal/animal_detail.html'

class AnimalDeleteView(DeleteView): 
    model = Animal
    success_url = reverse_lazy('animal-list')
    template_name = 'core/animal/animal_confirm_delete.html'

def animal_create(request):
    return generic_create_update_view(request, AnimalForm, 'Animal', 'core/animal/animal_form.html', 'animal-list')

def animal_update(request, pk):
    return generic_create_update_view(request, AnimalForm, 'Animal', 'core/animal/animal_form.html', 'animal-list', pk=pk)


# --- Especie Views ---
class EspecieListView(ListView): 
    model = Especie
    template_name = 'core/especie/especie_list.html'

class EspecieDetailView(DetailView): 
    model = Especie
    template_name = 'core/especie/especie_detail.html'

class EspecieDeleteView(DeleteView): 
    model = Especie
    success_url = reverse_lazy('especie-list')
    template_name = 'core/especie/especie_confirm_delete.html'

def especie_create(request):
    return generic_create_update_view(request, EspecieForm, 'Espécie', 'core/especie/especie_form.html', 'especie-list')

def especie_update(request, pk):
    return generic_create_update_view(request, EspecieForm, 'Espécie', 'core/especie/especie_form.html', 'especie-list', pk=pk)