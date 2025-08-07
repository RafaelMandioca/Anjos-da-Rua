# core/views/veterinario.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from ..models import Veterinario, CRMV
from ..forms.form_veterinario import VeterinarioForm, CrmvForm
from .cadastros_gerais import generic_create_update_view

# --- Veterinario Views ---
class VeterinarioListView(ListView): model = Veterinario; template_name = 'core/veterinario/veterinario_list.html'
class VeterinarioDetailView(DetailView): model = Veterinario; template_name = 'core/veterinario/veterinario_detail.html'
class VeterinarioDeleteView(DeleteView): model = Veterinario; success_url = reverse_lazy('veterinario-list'); template_name = 'core/veterinario/veterinario_confirm_delete.html'

def veterinario_create(request):
    if request.method == 'POST':
        veterinario_form = VeterinarioForm(request.POST, prefix='veterinario')
        crmv_form = CrmvForm(request.POST, prefix='crmv')
        if veterinario_form.is_valid() and crmv_form.is_valid():
            try:
                with transaction.atomic():
                    crmv = crmv_form.save()
                    veterinario = veterinario_form.save(commit=False)
                    veterinario.crmv = crmv
                    veterinario.save()
                return redirect('veterinario-list')
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
    else:
        veterinario_form = VeterinarioForm(prefix='veterinario')
        crmv_form = CrmvForm(prefix='crmv')
    context = {
        'veterinario_form': veterinario_form,
        'crmv_form': crmv_form,
        'form_title': 'Adicionar Veterinário'
    }
    return render(request, 'core/veterinario/veterinario_form_custom.html', context)

# A view de update para Veterinario precisa de uma lógica customizada similar
def veterinario_update(request, pk):
    veterinario_instance = get_object_or_404(Veterinario, pk=pk)
    crmv_instance = veterinario_instance.crmv
    
    if request.method == 'POST':
        veterinario_form = VeterinarioForm(request.POST, instance=veterinario_instance, prefix='veterinario')
        crmv_form = CrmvForm(request.POST, instance=crmv_instance, prefix='crmv')
        if veterinario_form.is_valid() and crmv_form.is_valid():
            with transaction.atomic():
                crmv_form.save()
                veterinario_form.save()
            return redirect('veterinario-list')
    else:
        veterinario_form = VeterinarioForm(instance=veterinario_instance, prefix='veterinario')
        crmv_form = CrmvForm(instance=crmv_instance, prefix='crmv')
        
    context = {
        'veterinario_form': veterinario_form,
        'crmv_form': crmv_form,
        'form_title': 'Editar Veterinário'
    }
    return render(request, 'core/veterinario/veterinario_form_custom.html', context)

# --- CRMV Views ---
class CrmvListView(ListView): model = CRMV
class CrmvDetailView(DetailView): model = CRMV
class CrmvDeleteView(DeleteView): model = CRMV; success_url = reverse_lazy('crmv-list')

def crmv_create(request):
    return generic_create_update_view(request, CrmvForm, 'CRMV', 'core/basic_form.html', 'crmv-list')

def crmv_update(request, pk):
    return generic_create_update_view(request, CrmvForm, 'CRMV', 'core/basic_form.html', 'crmv-list', pk=pk)
