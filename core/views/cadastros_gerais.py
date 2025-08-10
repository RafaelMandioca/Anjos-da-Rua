# core/views/cadastros_gerais.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction

from .mixins import SortableListViewMixin
from ..models import Endereco, Abrigo
from ..forms.form_cadastros_gerais import EnderecoForm, AbrigoForm

def is_admin(user):
    return user.is_authenticated and user.is_superuser

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)

@login_required
def index(request):
    if request.user.is_superuser:
        return redirect('gerenciamento')
    else:
        return redirect('abrigo-list')

def generic_create_update_view(request, model_form, title, template, redirect_url, pk=None):
    instance = None
    if pk:
        model_class = model_form._meta.model
        instance = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = model_form(instance=instance)

    context = {
        'form': form,
        'form_title': f"{'Editar' if pk else 'Adicionar'} {title}"
    }
    return render(request, template, context)

@login_required
@user_passes_test(is_admin)
def gerenciamento(request):
    return render(request, 'core/gerenciamento.html')

# --- Views para o modelo Abrigo ---
class AbrigoListView(LoginRequiredMixin, SortableListViewMixin, ListView):
    model = Abrigo
    template_name = 'core/abrigo/abrigo_list.html'
class AbrigoDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView): model = Abrigo; template_name = 'core/abrigo/abrigo_detail.html'
class AbrigoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView): model = Abrigo; success_url = reverse_lazy('abrigo-list'); template_name = 'core/abrigo/abrigo_confirm_delete.html'

@login_required
@user_passes_test(is_admin)
def abrigo_create_update(request, pk=None):
    instance = None
    endereco_instance = None
    if pk:
        instance = get_object_or_404(Abrigo, pk=pk)
        endereco_instance = instance.endereco

    if request.method == 'POST':
        abrigo_form = AbrigoForm(request.POST, instance=instance, prefix='abrigo')
        endereco_form = EnderecoForm(request.POST, instance=endereco_instance, prefix='endereco')
        
        if abrigo_form.is_valid() and endereco_form.is_valid():
            with transaction.atomic():
                endereco = endereco_form.save()
                abrigo = abrigo_form.save(commit=False)
                abrigo.endereco = endereco
                abrigo.save()
            return redirect('abrigo-list')
    else:
        abrigo_form = AbrigoForm(instance=instance, prefix='abrigo')
        endereco_form = EnderecoForm(instance=endereco_instance, prefix='endereco')

    context = {
        'abrigo_form': abrigo_form,
        'endereco_form': endereco_form,
        'form_title': f"{'Editar' if pk else 'Adicionar'} Abrigo"
    }
    return render(request, 'core/abrigo/abrigo_form.html', context)
