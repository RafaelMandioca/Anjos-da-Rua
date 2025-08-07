# core/views/atendimento.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from ..models import AtendimentoVeterinario, TipoConsulta
from ..forms.form_atendimento import AtendimentoVeterinarioForm, ItemAtendimentoFormSet, TipoConsultaForm
from .cadastros_gerais import generic_create_update_view

# --- Atendimento Views ---
class AtendimentoVeterinarioListView(ListView): model = AtendimentoVeterinario
class AtendimentoVeterinarioDetailView(DetailView): model = AtendimentoVeterinario
class AtendimentoVeterinarioDeleteView(DeleteView): model = AtendimentoVeterinario; success_url = reverse_lazy('atendimentoveterinario-list')

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
class TipoConsultaListView(ListView): model = TipoConsulta
class TipoConsultaDetailView(DetailView): model = TipoConsulta
class TipoConsultaDeleteView(DeleteView): model = TipoConsulta; success_url = reverse_lazy('tipoconsulta-list')

def tipoconsulta_create(request):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/generic_form.html', 'tipoconsulta-list')

def tipoconsulta_update(request, pk):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/generic_form.html', 'tipoconsulta-list', pk=pk)
