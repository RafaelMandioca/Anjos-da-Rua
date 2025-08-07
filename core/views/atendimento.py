# core/views/atendimento.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from ..models import AtendimentoVeterinario, TipoConsulta
from ..forms.form_atendimento import AtendimentoVeterinarioForm, ItemAtendimentoFormSet, TipoConsultaForm
from .cadastros_gerais import generic_create_update_view

# --- Atendimento Views ---
class AtendimentoVeterinarioListView(ListView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_list.html'

class AtendimentoVeterinarioDetailView(DetailView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_detail.html'

class AtendimentoVeterinarioDeleteView(DeleteView): 
    model = AtendimentoVeterinario
    success_url = reverse_lazy('atendimentoveterinario-list')
    template_name = 'core/atendimento/atendimento_confirm_delete.html'

def atendimento_veterinario_create_update(request, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(AtendimentoVeterinario, pk=pk)
    
    if request.method == 'POST':
        form = AtendimentoVeterinarioForm(request.POST, instance=instance)
        formset = ItemAtendimentoFormSet(request.POST, instance=instance)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                atendimento = form.save()
                formset.instance = atendimento
                formset.save()
            return redirect('atendimentoveterinario-list')
    else:
        form = AtendimentoVeterinarioForm(instance=instance)
        formset = ItemAtendimentoFormSet(instance=instance)

    context = {
        'form': form,
        'formset': formset,
        'form_title': f"{'Editar' if pk else 'Adicionar'} Atendimento"
    }
    return render(request, 'core/atendimento/atendimento_form.html', context)

# --- TipoConsulta Views ---
class TipoConsultaListView(ListView): 
    model = TipoConsulta
    template_name = 'core/tipoconsulta/tipoconsulta_list.html'

class TipoConsultaDetailView(DetailView): 
    model = TipoConsulta
    template_name = 'core/tipoconsulta/tipoconsulta_detail.html'

class TipoConsultaDeleteView(DeleteView): 
    model = TipoConsulta
    success_url = reverse_lazy('tipoconsulta-list')
    template_name = 'core/tipoconsulta/tipoconsulta_confirm_delete.html'

def tipoconsulta_create(request):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/tipoconsulta/tipoconsulta_form.html', 'tipoconsulta-list')

def tipoconsulta_update(request, pk):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/tipoconsulta/tipoconsulta_form.html', 'tipoconsulta-list', pk=pk)