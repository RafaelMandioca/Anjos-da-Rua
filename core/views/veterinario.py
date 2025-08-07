# core/views/veterinario.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from ..models import Veterinario, CRMV, Endereco
from ..forms.form_veterinario import VeterinarioForm, CrmvForm
from ..forms.form_cadastros_gerais import EnderecoForm # Importar o EnderecoForm
from .cadastros_gerais import generic_create_update_view

# --- Veterinario Views ---
class VeterinarioListView(ListView): model = Veterinario; template_name = 'core/veterinario/veterinario_list.html'
class VeterinarioDetailView(DetailView): model = Veterinario; template_name = 'core/veterinario/veterinario_detail.html'
class VeterinarioDeleteView(DeleteView): model = Veterinario; success_url = reverse_lazy('veterinario-list'); template_name = 'core/veterinario/veterinario_confirm_delete.html'

def veterinario_create(request):
    if request.method == 'POST':
        veterinario_form = VeterinarioForm(request.POST, prefix='veterinario')
        crmv_form = CrmvForm(request.POST, prefix='crmv')
        endereco_form = EnderecoForm(request.POST, prefix='endereco')

        if veterinario_form.is_valid() and crmv_form.is_valid() and endereco_form.is_valid():
            try:
                with transaction.atomic():
                    # Salva o endereço e o crmv primeiro
                    endereco = endereco_form.save()
                    crmv = crmv_form.save()
                    
                    # Cria o veterinário, mas não salva ainda (commit=False)
                    veterinario = veterinario_form.save(commit=False)
                    # Associa o crmv e o endereço criados
                    veterinario.crmv = crmv
                    veterinario.endereco = endereco
                    # Salva o veterinário
                    veterinario.save()
                return redirect('veterinario-list')
            except Exception as e:
                # Em caso de erro, a transação é desfeita (rollback)
                print(f"Ocorreu um erro: {e}")
    else:
        veterinario_form = VeterinarioForm(prefix='veterinario')
        crmv_form = CrmvForm(prefix='crmv')
        endereco_form = EnderecoForm(prefix='endereco')

    context = {
        'veterinario_form': veterinario_form,
        'crmv_form': crmv_form,
        'endereco_form': endereco_form,
        'form_title': 'Adicionar Veterinário'
    }
    return render(request, 'core/veterinario/veterinario_form_custom.html', context)

def veterinario_update(request, pk):
    veterinario_instance = get_object_or_404(Veterinario, pk=pk)
    crmv_instance = veterinario_instance.crmv
    endereco_instance = veterinario_instance.endereco
    
    if request.method == 'POST':
        veterinario_form = VeterinarioForm(request.POST, instance=veterinario_instance, prefix='veterinario')
        crmv_form = CrmvForm(request.POST, instance=crmv_instance, prefix='crmv')
        endereco_form = EnderecoForm(request.POST, instance=endereco_instance, prefix='endereco')

        if veterinario_form.is_valid() and crmv_form.is_valid() and endereco_form.is_valid():
            with transaction.atomic():
                endereco_form.save()
                crmv_form.save()
                veterinario_form.save()
            return redirect('veterinario-list')
    else:
        veterinario_form = VeterinarioForm(instance=veterinario_instance, prefix='veterinario')
        crmv_form = CrmvForm(instance=crmv_instance, prefix='crmv')
        endereco_form = EnderecoForm(instance=endereco_instance, prefix='endereco')
        
    context = {
        'veterinario_form': veterinario_form,
        'crmv_form': crmv_form,
        'endereco_form': endereco_form,
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