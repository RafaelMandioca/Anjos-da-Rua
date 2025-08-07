# core/views/cadastros_gerais.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from ..models import Cidade, Endereco, Abrigo
from ..forms.form_cadastros_gerais import CidadeForm, EnderecoForm, AbrigoForm

def index(request):
    return render(request, 'core/index.html')

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

# --- Views para o modelo Cidade ---

class CidadeListView(ListView):
    model = Cidade
    template_name = 'core/cidade/cidade_list.html'

class CidadeDetailView(DetailView):
    model = Cidade
    template_name = 'core/cidade/cidade_detail.html'

class CidadeDeleteView(DeleteView):
    model = Cidade
    success_url = reverse_lazy('cidade-list')
    template_name = 'core/cidade/cidade_confirm_delete.html'

def cidade_create(request):
    return generic_create_update_view(request, CidadeForm, 'Cidade', 'core/cidade/cidade_form.html', 'cidade-list')

def cidade_update(request, pk):
    return generic_create_update_view(request, CidadeForm, 'Cidade', 'core/cidade/cidade_form.html', 'cidade-list', pk=pk)

# --- Views para o modelo Endereco ---

class EnderecoListView(ListView):
    model = Endereco
    template_name = 'core/endereco/endereco_list.html'

class EnderecoDetailView(DetailView):
    model = Endereco
    template_name = 'core/endereco/endereco_detail.html'

class EnderecoDeleteView(DeleteView):
    model = Endereco
    success_url = reverse_lazy('endereco-list')
    template_name = 'core/endereco/endereco_confirm_delete.html'

def endereco_create(request):
    return generic_create_update_view(request, EnderecoForm, 'Endereço', 'core/endereco/endereco_form.html', 'endereco-list')

def endereco_update(request, pk):
    return generic_create_update_view(request, EnderecoForm, 'Endereço', 'core/endereco/endereco_form.html', 'endereco-list', pk=pk)

# --- Views para o modelo Abrigo ---

class AbrigoListView(ListView):
    model = Abrigo
    template_name = 'core/abrigo/abrigo_list.html'

class AbrigoDetailView(DetailView):
    model = Abrigo
    template_name = 'core/abrigo/abrigo_detail.html'

class AbrigoDeleteView(DeleteView):
    model = Abrigo
    success_url = reverse_lazy('abrigo-list')
    template_name = 'core/abrigo/abrigo_confirm_delete.html'

def abrigo_create(request):
    return generic_create_update_view(request, AbrigoForm, 'Abrigo', 'core/abrigo/abrigo_form.html', 'abrigo-list')

def abrigo_update(request, pk):
    return generic_create_update_view(request, AbrigoForm, 'Abrigo', 'core/abrigo/abrigo_form.html', 'abrigo-list', pk=pk)