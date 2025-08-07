# core/views/cadastros_gerais.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy

# Imports relativos para buscar os modelos e formulários da pasta 'core'
from ..models import Cidade, Endereco, Abrigo
from ..forms.form_cadastros_gerais import CidadeForm, EnderecoForm, AbrigoForm

def index(request):
    """
    Renderiza a página inicial do projeto.
    """
    return render(request, 'core/index.html')

def generic_create_update_view(request, model_form, title, template, redirect_url, pk=None):
    """
    Uma view genérica para criar e atualizar instâncias de modelos simples.
    - `pk=None` indica uma operação de criação.
    - `pk` com valor indica uma operação de atualização.
    """
    instance = None
    if pk:
        # Se um 'pk' (primary key) for fornecido, busca o objeto existente no banco de dados.
        model_class = model_form._meta.model
        instance = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        # Se o formulário for submetido (método POST), cria uma instância do formulário
        # com os dados enviados (request.POST) e a instância do modelo (se for edição).
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            # Se o formulário for válido, salva os dados no banco de dados.
            form.save()
            # Redireciona para a URL de sucesso (geralmente a lista do modelo).
            return redirect(redirect_url)
    else:
        # Se for uma requisição GET, cria um formulário em branco (para criação)
        # ou preenchido com os dados da instância (para edição).
        form = model_form(instance=instance)

    # Prepara o contexto para ser enviado ao template.
    context = {
        'form': form,
        'form_title': f"{'Editar' if pk else 'Adicionar'} {title}"
    }
    # Renderiza o template com o contexto.
    return render(request, template, context)

# --- Views para o modelo Cidade ---

class CidadeListView(ListView):
    model = Cidade

class CidadeDetailView(DetailView):
    model = Cidade

class CidadeDeleteView(DeleteView):
    model = Cidade
    success_url = reverse_lazy('cidade-list')

def cidade_create(request):
    """
    View para criar uma nova Cidade, utilizando a view genérica.
    """
    return generic_create_update_view(request, CidadeForm, 'Cidade', 'core/basic_form.html', 'cidade-list')

def cidade_update(request, pk):
    """
    View para editar uma Cidade existente, utilizando a view genérica.
    """
    return generic_create_update_view(request, CidadeForm, 'Cidade', 'core/basic_form.html', 'cidade-list', pk=pk)

# --- Views para o modelo Endereco ---

class EnderecoListView(ListView):
    model = Endereco

class EnderecoDetailView(DetailView):
    model = Endereco

class EnderecoDeleteView(DeleteView):
    model = Endereco
    success_url = reverse_lazy('endereco-list')

def endereco_create(request):
    """
    View para criar um novo Endereço, utilizando a view genérica.
    """
    return generic_create_update_view(request, EnderecoForm, 'Endereço', 'core/basic_form.html', 'endereco-list')

def endereco_update(request, pk):
    """
    View para editar um Endereço existente, utilizando a view genérica.
    """
    return generic_create_update_view(request, EnderecoForm, 'Endereço', 'core/basic_form.html', 'endereco-list', pk=pk)

# --- Views para o modelo Abrigo ---

class AbrigoListView(ListView):
    model = Abrigo

class AbrigoDetailView(DetailView):
    model = Abrigo

class AbrigoDeleteView(DeleteView):
    model = Abrigo
    success_url = reverse_lazy('abrigo-list')

def abrigo_create(request):
    """
    View para criar um novo Abrigo, utilizando a view genérica.
    """
    return generic_create_update_view(request, AbrigoForm, 'Abrigo', 'core/basic_form.html', 'abrigo-list')

def abrigo_update(request, pk):
    """
    View para editar um Abrigo existente, utilizando a view genérica.
    """
    return generic_create_update_view(request, AbrigoForm, 'Abrigo', 'core/basic_form.html', 'abrigo-list', pk=pk)