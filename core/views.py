from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cidade, Endereco, Abrigo, CRMV, Veterinario, Especie, Animal
from .models import TipoConsulta, Item, AtendimentoVeterinario,ItemHasAtendimentoVeterinario

class VeterinarioListView(ListView):
  model = Veterinario

class VeterinarioDetailView(DetailView):
  model = Veterinario

class VeterinarioCreateView(CreateView):
  model = Veterinario
  fields = ['nome', 'cpf', 'email', 'telefone', 'crmv', 'endereco']
  success_url = reverse_lazy('veterinario-list')

class VeterinarioUpdateView(UpdateView):
  model = Veterinario
  fields = ['nome', 'email', 'telefone', 'endereco']
  success_url = reverse_lazy('veterinario-list')

class VeterinarioDeleteView(DeleteView):
  model = Veterinario
  success_url = reverse_lazy('veterinario-list')

######################################################################

class AnimalListView(ListView):
  model = Animal

class AnimalDetailView(DetailView):
  model = Animal

class AnimalCreateView(CreateView):
  model = Animal
  fields = ['nome_apelido', 'peso', 'idade', 'sexo', 'especie']
  success_url = reverse_lazy('animal-list')

class AnimalUpdateView(UpdateView):
  model = Animal
  fields = ['nome_apelido', 'peso', 'idade']
  success_url = reverse_lazy('animal-list')

class AnimalDeleteView(DeleteView):
  model = Animal
  success_url = reverse_lazy('animal-list')

######################################################################

class EspecieListView(ListView):
    model = Especie

class EspecieDetailView(DetailView):
    model = Especie

class EspecieCreateView(CreateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'expectativa_de_vida', 'raca']
    success_url = reverse_lazy('especie-list')

class EspecieUpdateView(UpdateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'expectativa_de_vida', 'raca']
    success_url = reverse_lazy('especie-list')

class EspecieDeleteView(DeleteView):
    model = Especie
    success_url = reverse_lazy('especie-list')

######################################################################

class ItemListView(ListView):
  model = Item

class ItemDetailView(DetailView):
  model = Item

class ItemCreateView(CreateView):
  model = Item
  fields = ['nome', 'categoria', 'preco_unitario', 'dataValidade']
  success_url = reverse_lazy('item-list')

class ItemUpdateView(UpdateView):
  model = Item
  fields = ['preco_unitario']
  success_url = reverse_lazy('item-list')

class ItemDeleteView(DeleteView):
  model = Item
  success_url = reverse_lazy('item-list')
  
######################################################################

class CidadeListView(ListView):
  model = Cidade

class CidadeDetailView(DetailView):
  model = Cidade

class CidadeCreateView(CreateView):
  model = Cidade
  fields = ['nome', 'uf']
  success_url = reverse_lazy('cidade-list')

class CidadeUpdateView(UpdateView):
  model = Cidade
  fields = ['nome', 'uf']
  success_url = reverse_lazy('cidade-list')

class CidadeDeleteView(DeleteView):
  model = Cidade
  success_url = reverse_lazy('cidade-list')

######################################################################

class EnderecoListView(ListView):
  model = Endereco

class EnderecoDetailView(DetailView):
  model = Endereco

class EnderecoCreateView(CreateView):
  model = Endereco
  fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'ponto_de_referencia', 'cidade']
  success_url = reverse_lazy('endereco-list')

class EnderecoUpdateView(UpdateView):
  model = Endereco
  fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'ponto_de_referencia', 'cidade']
  success_url = reverse_lazy('endereco-list')

class EnderecoDeleteView(DeleteView):
  model = Endereco
  success_url = reverse_lazy('endereco-list')

######################################################################

class AbrigoListView(ListView):
  model = Abrigo

class AbrigoDetailView(DetailView):
  model = Abrigo

class AbrigoCreateView(CreateView):
  model = Abrigo
  fields = ['nome', 'endereco']
  success_url = reverse_lazy('abrigo-list')

class AbrigoUpdateView(UpdateView):
  model = Abrigo
  fields = ['nome', 'endereco']
  success_url = reverse_lazy('abrigo-list')

class AbrigoDeleteView(DeleteView):
  model = Abrigo
  success_url = reverse_lazy('abrigo-list')

######################################################################

class CrmvListView(ListView):
  model = CRMV

class CrmvDetailView(DetailView):
  model = CRMV

class CrmvCreateView(CreateView):
  model = CRMV
  fields = ['numero', 'estado']
  success_url = reverse_lazy('crmv-list')

class CrmvUpdateView(UpdateView):
  model = CRMV
  fields = ['numero', 'estado']
  success_url = reverse_lazy('crmv-list')

class CrmvDeleteView(DeleteView):
  model = CRMV
  success_url = reverse_lazy('crmv-list')

######################################################################

class TipoConsultaListView(ListView):
  model = TipoConsulta

class TipoConsultaDetailView(DetailView):
  model = TipoConsulta

class TipoConsultaCreateView(CreateView):
  model = TipoConsulta
  fields = ['descricao']
  success_url = reverse_lazy('tipoconsulta-list')

class TipoConsultaUpdateView(UpdateView):
  model = TipoConsulta
  fields = ['descricao']
  success_url = reverse_lazy('tipoconsulta-list')

class TipoConsultaDeleteView(DeleteView):
  model = TipoConsulta
  success_url = reverse_lazy('tipoconsulta-list')

######################################################################

class AtendimentoVeterinarioListView(ListView):
  model = AtendimentoVeterinario

class AtendimentoVeterinarioDetailView(DetailView):
  model = AtendimentoVeterinario

class AtendimentoVeterinarioCreateView(CreateView):
  model = AtendimentoVeterinario
  fields = ['data_do_atendimento', 'observacoes', 'Veterinario_idVeterinario', 'TipoConsulta_idTipoConsulta', 'Animal_idAnimal']
  success_url = reverse_lazy('atendimentoveterinario-list')

class AtendimentoVeterinarioUpdateView(UpdateView):
  model = AtendimentoVeterinario
  fields = ['data_do_atendimento', 'observacoes']
  success_url = reverse_lazy('atendimentoveterinario-list')

class AtendimentoVeterinarioDeleteView(DeleteView):
  model = AtendimentoVeterinario
  success_url = reverse_lazy('atendimentoveterinario-list')
