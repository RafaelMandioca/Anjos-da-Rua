# core/views/atendimento.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SortableListViewMixin
from ..models import AtendimentoVeterinario, TipoConsulta, Animal
from ..forms.form_atendimento import (
    AtendimentoVeterinarioForm, 
    VeterinarioAtendimentoForm,
    ItemAtendimentoFormSet, 
    TipoConsultaForm
)
from .cadastros_gerais import generic_create_update_view

# --- Atendimento Views ---
class AtendimentoVeterinarioListView(LoginRequiredMixin, SortableListViewMixin, ListView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_list.html'

class AtendimentoVeterinarioDetailView(LoginRequiredMixin, DetailView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_detail.html'

class AtendimentoVeterinarioDeleteView(LoginRequiredMixin, DeleteView): 
    model = AtendimentoVeterinario
    success_url = reverse_lazy('atendimentoveterinario-list')
    template_name = 'core/atendimento/atendimento_confirm_delete.html'

def atendimento_veterinario_create_update(request, pk=None):
    instance = get_object_or_404(AtendimentoVeterinario, pk=pk) if pk else None
    
    quantidades_antigas = {
        item.item.id: item.quantidade 
        for item in instance.itemhasatendimentoveterinario_set.all()
    } if instance else {}

    FormClass = AtendimentoVeterinarioForm if request.user.is_superuser else VeterinarioAtendimentoForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance)
        formset = ItemAtendimentoFormSet(request.POST, instance=instance)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    atendimento = form.save(commit=False)
                    if not request.user.is_superuser:
                        atendimento.veterinario = request.user
                    atendimento.save()

                    # Devolve o estoque dos itens removidos
                    for form_deletado in formset.deleted_forms:
                        item_instancia = form_deletado.instance
                        if item_instancia.pk: 
                            item_instancia.item.quantidade = F('quantidade') + item_instancia.quantidade
                            item_instancia.item.save()

                    # Processa os itens novos ou modificados
                    for item_form in formset.cleaned_data:
                        if not item_form or item_form.get('DELETE'):
                            continue
                        
                        item_obj = item_form['item']
                        quantidade_nova = item_form['quantidade']
                        item_id = item_obj.id
                        
                        quantidade_antiga = quantidades_antigas.get(item_id, 0)
                        diferenca = quantidade_nova - quantidade_antiga
                        
                        item_obj.refresh_from_db()
                        if item_obj.quantidade < diferenca:
                            form.add_error(None, f"Estoque insuficiente para o item {item_obj.nome}. Disponível: {item_obj.quantidade}")
                            raise transaction.TransactionManagementError()

                        item_obj.quantidade = F('quantidade') - diferenca
                        item_obj.save()

                    formset.instance = atendimento
                    formset.save()
                return redirect('atendimentoveterinario-list')
            except transaction.TransactionManagementError:
                pass
    else:
        form = FormClass(instance=instance)
        formset = ItemAtendimentoFormSet(instance=instance)

    context = {
        'form': form,
        'formset': formset,
        'form_title': f"{'Editar' if pk else 'Adicionar'} Atendimento"
    }
    return render(request, 'core/atendimento/atendimento_form.html', context)

# --- TipoConsulta Views ---
class TipoConsultaListView(LoginRequiredMixin, SortableListViewMixin, ListView): 
    model = TipoConsulta
    template_name = 'core/tipoconsulta/tipoconsulta_list.html'
class TipoConsultaDetailView(LoginRequiredMixin, DetailView): model = TipoConsulta; template_name = 'core/tipoconsulta/tipoconsulta_detail.html'
class TipoConsultaDeleteView(LoginRequiredMixin, DeleteView): model = TipoConsulta; success_url = reverse_lazy('tipoconsulta-list'); template_name = 'core/tipoconsulta/tipoconsulta_confirm_delete.html'

def tipoconsulta_create(request):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/tipoconsulta/tipoconsulta_form.html', 'tipoconsulta-list')

def tipoconsulta_update(request, pk):
    return generic_create_update_view(request, TipoConsultaForm, 'Tipo de Consulta', 'core/tipoconsulta/tipoconsulta_form.html', 'tipoconsulta-list', pk=pk)