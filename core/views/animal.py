# core/views/animal.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from .mixins import SortableListViewMixin
from ..models import Animal, Especie, Abrigo
from ..forms.form_animal import AnimalForm, EspecieForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# --- Animal Views ---
class AnimalListView(LoginRequiredMixin, AdminRequiredMixin, SortableListViewMixin, ListView): 
    model = Animal
    template_name = 'core/animal/animal_list.html'
    
class AnimalDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView): 
    model = Animal
    template_name = 'core/animal/animal_detail.html'

class AnimalDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView): 
    model = Animal
    success_url = reverse_lazy('animal-list')
    template_name = 'core/animal/animal_confirm_delete.html'

def animal_create_update(request, pk=None):
    instance = None
    especie_instance = None
    if pk:
        instance = get_object_or_404(Animal, pk=pk)
        especie_instance = instance.especie

    if request.method == 'POST':
        animal_form = AnimalForm(request.POST, instance=instance, prefix='animal')
        especie_form = EspecieForm(request.POST, instance=especie_instance, prefix='especie')
        
        if animal_form.is_valid() and especie_form.is_valid():
            with transaction.atomic():
                especie = especie_form.save()
                animal = animal_form.save(commit=False)
                animal.especie = especie
                animal.save()
            return redirect('animal-list')
    else:
        animal_form = AnimalForm(instance=instance, prefix='animal')
        especie_form = EspecieForm(instance=especie_instance, prefix='especie')

    context = {
        'animal_form': animal_form,
        'especie_form': especie_form,
        'form_title': f"{'Editar' if pk else 'Adicionar'} Animal e Espécie"
    }
    return render(request, 'core/animal/animal_form.html', context)

# --- AnimalPorAbrigo View ---
class AnimalPorAbrigoListView(LoginRequiredMixin, SortableListViewMixin, ListView):
    model = Animal
    template_name = 'core/animal/animal_list_por_abrigo.html'
    context_object_name = 'animal_list'

    def get_queryset(self):
        return Animal.objects.filter(abrigo_id=self.kwargs['abrigo_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['abrigo'] = get_object_or_404(Abrigo, pk=self.kwargs['abrigo_id'])
        return context
