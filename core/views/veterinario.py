# core/views/veterinario.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .mixins import SortableListViewMixin
from ..models import Veterinario, CRMV, Endereco
from ..forms.form_veterinario import VeterinarioForm, CrmvForm, VeterinarioUpdateForm
from ..forms.form_cadastros_gerais import EnderecoForm
from .cadastros_gerais import generic_create_update_view, AdminRequiredMixin, is_admin

class VeterinarioOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        veterinario = self.get_object()
        return self.request.user == veterinario

@login_required
def perfil_view(request):
    section = request.GET.get('section', 'info') 
    context = {'section': section}
    return render(request, 'core/veterinario/perfil.html', context)

@login_required
def perfil_alterar_endereco(request):
    veterinario = get_object_or_404(Veterinario, pk=request.user.pk)
    endereco_instance = veterinario.endereco or None

    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco_instance)
        if form.is_valid():
            endereco = form.save()
            if not veterinario.endereco:
                veterinario.endereco = endereco
                veterinario.save()
            messages.success(request, 'Endereço atualizado com sucesso!')
            return redirect('perfil_alterar_endereco')
    else:
        form = EnderecoForm(instance=endereco_instance)

    context = {
        'form': form,
        'form_title': 'Alterar Endereço',
        'section': 'endereco'
    }
    return render(request, 'core/veterinario/perfil_form.html', context)

@login_required
def perfil_alterar_informacoes(request):
    veterinario = get_object_or_404(Veterinario, pk=request.user.pk)
    if request.method == 'POST':
        form = VeterinarioUpdateForm(request.POST, instance=veterinario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações atualizadas com sucesso!')
            return redirect('perfil_alterar_informacoes')
    else:
        form = VeterinarioUpdateForm(instance=veterinario)
    
    context = {
        'form': form,
        'form_title': 'Alterar Informações',
        'section': 'info'
    }
    return render(request, 'core/veterinario/perfil_form.html', context)

@login_required
def perfil_alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil_alterar_senha')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'form_title': 'Alterar Senha',
        'section': 'senha'
    }
    return render(request, 'core/veterinario/perfil_form.html', context)

class PerfilDeleteView(LoginRequiredMixin, DeleteView):
    model = Veterinario
    success_url = reverse_lazy('login')
    template_name = 'core/veterinario/perfil_confirm_delete.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'apagar'
        return context

# --- Veterinario Views ---
class VeterinarioListView(LoginRequiredMixin, SortableListViewMixin, ListView): 
    model = Veterinario
    template_name = 'core/veterinario/veterinario_list.html'
class VeterinarioDetailView(LoginRequiredMixin, DetailView): model = Veterinario; template_name = 'core/veterinario/veterinario_detail.html'
class VeterinarioDeleteView(LoginRequiredMixin, VeterinarioOrAdminMixin, DeleteView): model = Veterinario; success_url = reverse_lazy('veterinario-list'); template_name = 'core/veterinario/veterinario_confirm_delete.html'

@login_required
@user_passes_test(is_admin)
def veterinario_create(request):
    if request.method == 'POST':
        veterinario_form = VeterinarioForm(request.POST, prefix='veterinario')
        crmv_form = CrmvForm(request.POST, prefix='crmv')
        endereco_form = EnderecoForm(request.POST, prefix='endereco')

        if veterinario_form.is_valid() and crmv_form.is_valid() and endereco_form.is_valid():
            try:
                with transaction.atomic():
                    endereco = endereco_form.save()
                    crmv = crmv_form.save()
                    veterinario = veterinario_form.save(commit=False)
                    veterinario.crmv = crmv
                    veterinario.endereco = endereco
                    veterinario.save()
                return redirect('veterinario-list')
            except Exception as e:
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

@login_required
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
class CrmvListView(LoginRequiredMixin, AdminRequiredMixin, SortableListViewMixin, ListView): 
    model = CRMV
    template_name = 'core/crmv/crmv_list.html'
class CrmvDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView): model = CRMV; template_name = 'core/crmv/crmv_detail.html'
class CrmvDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView): model = CRMV; success_url = reverse_lazy('crmv-list'); template_name = 'core/crmv/crmv_confirm_delete.html'

@login_required
@user_passes_test(is_admin)
def crmv_create(request):
    return generic_create_update_view(request, CrmvForm, 'CRMV', 'core/crmv/crmv_form.html', 'crmv-list')

@login_required
@user_passes_test(is_admin)
def crmv_update(request, pk):
    return generic_create_update_view(request, CrmvForm, 'CRMV', 'core/crmv/crmv_form.html', 'crmv-list', pk=pk)