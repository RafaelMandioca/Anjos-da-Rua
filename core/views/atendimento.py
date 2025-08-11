# core/views/atendimento.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .mixins import SortableListViewMixin
from ..models import AtendimentoVeterinario, TipoConsulta, Animal, StatusAtendimento
from ..forms.form_atendimento import (
    AtendimentoVeterinarioForm, 
    VeterinarioAtendimentoForm,
    ItemAtendimentoFormSet, 
    TipoConsultaForm
)
from .cadastros_gerais import generic_create_update_view, AdminRequiredMixin

# --- Mixin de Permissão ---
class VeterinarioIsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        atendimento = self.get_object()
        return self.request.user.is_superuser or self.request.user == atendimento.veterinario

# --- Atendimento Views ---
class AtendimentoVeterinarioListView(LoginRequiredMixin, AdminRequiredMixin, SortableListViewMixin, ListView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_list.html'

class AtendimentoPorAnimalListView(LoginRequiredMixin, SortableListViewMixin, ListView):
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_list_por_animal.html'
    context_object_name = 'atendimento_list'

    def get_queryset(self):
        self.animal = get_object_or_404(Animal, pk=self.kwargs['animal_id'])
        queryset = AtendimentoVeterinario.objects.filter(animal=self.animal)
        
        if not self.request.user.is_superuser:
            queryset = queryset.filter(veterinario=self.request.user)
            
        return queryset.order_by('-data_do_atendimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animal'] = self.animal
        return context

class AtendimentoVeterinarioDetailView(LoginRequiredMixin, VeterinarioIsOwnerOrAdminMixin, DetailView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.META.get('HTTP_REFERER', reverse_lazy('abrigo-list'))
        return context

class AtendimentoVeterinarioDeleteView(LoginRequiredMixin, VeterinarioIsOwnerOrAdminMixin, DeleteView): 
    model = AtendimentoVeterinario
    template_name = 'core/atendimento/atendimento_confirm_delete.html'

    def get_success_url(self):
        redirect_url = self.request.POST.get('next', None)
        if redirect_url:
            return redirect_url
        if self.request.user.is_superuser:
            return reverse_lazy('atendimentoveterinario-list')
        return reverse_lazy('abrigo-list')

    def form_valid(self, form):
        atendimento = self.get_object()
        if atendimento.status and atendimento.status.descricao == 'Concluído':
            with transaction.atomic():
                for item_atendimento in atendimento.itemhasatendimentoveterinario_set.all():
                    item = item_atendimento.item
                    item.quantidade = F('quantidade') + item_atendimento.quantidade
                    item.save()
            messages.success(self.request, "Atendimento concluído excluído e itens retornados ao estoque.")
        else:
            messages.success(self.request, "Atendimento não concluído excluído com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.META.get('HTTP_REFERER', reverse_lazy('abrigo-list'))
        return context

def atendimento_veterinario_create_update(request, pk=None):
    instance = get_object_or_404(AtendimentoVeterinario, pk=pk) if pk else None
    
    if instance and not (request.user.is_superuser or request.user == instance.veterinario):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    animal_id = request.GET.get('animal_id') or request.POST.get('animal_id')
    initial_animal = get_object_or_404(Animal, pk=animal_id) if animal_id else None

    original_status_is_concluido = instance and instance.status and instance.status.descricao == 'Concluído'
    FormClass = AtendimentoVeterinarioForm if request.user.is_superuser else VeterinarioAtendimentoForm
    back_url = request.POST.get('next', request.META.get('HTTP_REFERER', reverse_lazy('abrigo-list')))

    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance, user=request.user, initial_animal=initial_animal)
        formset = ItemAtendimentoFormSet(request.POST, instance=instance)
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    atendimento = form.save(commit=False)
                    
                    if initial_animal and not instance:
                        atendimento.animal = initial_animal

                    if not atendimento.pk:
                        atendimento.status = StatusAtendimento.objects.get(descricao='Não Concluído')

                    if not request.user.is_superuser:
                        atendimento.veterinario = request.user
                    
                    atendimento.save()
                    formset.instance = atendimento
                    formset.save()

                    novo_status_obj = form.cleaned_data.get('status')
                    novo_status_e_concluido = novo_status_obj and novo_status_obj.descricao == 'Concluído'

                    if not original_status_is_concluido and novo_status_e_concluido:
                        for item_atendimento in atendimento.itemhasatendimentoveterinario_set.all():
                            item = item_atendimento.item
                            quantidade_a_deduzir = item_atendimento.quantidade
                            
                            item.refresh_from_db()
                            if item.quantidade < quantidade_a_deduzir:
                                messages.error(request, f"Estoque insuficiente para concluir o atendimento com o item '{item.nome}'. "
                                                        f"Necessário: {quantidade_a_deduzir}, Disponível: {item.quantidade}.")
                                raise transaction.TransactionManagementError("Estoque insuficiente")
                            
                            item.quantidade = F('quantidade') - quantidade_a_deduzir
                            item.save()
                        messages.success(request, 'Atendimento concluído e estoque atualizado com sucesso!')
                    else:
                        messages.success(request, 'Atendimento salvo com sucesso!')
                
                redirect_url = request.POST.get('next', reverse_lazy('abrigo-list' if not request.user.is_superuser else 'atendimentoveterinario-list'))
                return redirect(redirect_url)

            except transaction.TransactionManagementError:
                pass
    else:
        form = FormClass(instance=instance, user=request.user, initial_animal=initial_animal)
        formset = ItemAtendimentoFormSet(instance=instance)

    context = {
        'form': form,
        'formset': formset,
        'form_title': f"{'Editar' if pk else 'Adicionar'} Atendimento",
        'back_url': back_url,
        'is_concluido': original_status_is_concluido,
        'initial_animal_id': animal_id,
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