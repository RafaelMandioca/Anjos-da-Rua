from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import (
    Cidade, Endereco, Abrigo, CRMV, Veterinario, Especie, Animal,
    TipoConsulta, Item, AtendimentoVeterinario, ItemHasAtendimentoVeterinario
)

def index(request):
  return render(request, 'core/index.html')

######################################################################
# Veterinario Views
######################################################################

class VeterinarioListView(ListView):
  model = Veterinario
  template_name = 'core/veterinario/veterinario_list.html'

class VeterinarioDetailView(DetailView):
  model = Veterinario
  template_name = 'core/veterinario/veterinario_detail.html'

class VeterinarioCreateView(CreateView):
  model = Veterinario
  fields = ['nome', 'cpf', 'email', 'telefone', 'crmv', 'endereco']
  success_url = reverse_lazy('veterinario-list')
  template_name = 'core/veterinario/veterinario_form.html'

class VeterinarioUpdateView(UpdateView):
  model = Veterinario
  fields = ['nome', 'email', 'telefone', 'endereco']
  success_url = reverse_lazy('veterinario-list')
  template_name = 'core/veterinario/veterinario_form.html'

class VeterinarioDeleteView(DeleteView):
  model = Veterinario
  success_url = reverse_lazy('veterinario-list')
  template_name = 'core/veterinario/veterinario_confirm_delete.html'

######################################################################
# Animal Views
######################################################################

class AnimalListView(ListView):
  model = Animal
  template_name = 'core/animal/animal_list.html'

class AnimalDetailView(DetailView):
  model = Animal
  template_name = 'core/animal/animal_detail.html'

class AnimalCreateView(CreateView):
  model = Animal
  fields = ['nome_apelido', 'peso', 'idade', 'sexo', 'especie']
  success_url = reverse_lazy('animal-list')
  template_name = 'core/animal/animal_form.html'

class AnimalUpdateView(UpdateView):
  model = Animal
  fields = ['nome_apelido', 'peso', 'idade']
  success_url = reverse_lazy('animal-list')
  template_name = 'core/animal/animal_form.html'

class AnimalDeleteView(DeleteView):
  model = Animal
  success_url = reverse_lazy('animal-list')
  template_name = 'core/animal/animal_confirm_delete.html'

######################################################################
# Especie Views
######################################################################

class EspecieListView(ListView):
    model = Especie
    template_name = 'core/especie/especie_list.html'

class EspecieDetailView(DetailView):
    model = Especie
    template_name = 'core/especie/especie_detail.html'

class EspecieCreateView(CreateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'expectativa_de_vida', 'raca']
    success_url = reverse_lazy('especie-list')
    template_name = 'core/especie/especie_form.html'

class EspecieUpdateView(UpdateView):
    model = Especie
    fields = ['nome_comum', 'nome_cientifico', 'expectativa_de_vida', 'raca']
    success_url = reverse_lazy('especie-list')
    template_name = 'core/especie/especie_form.html'

class EspecieDeleteView(DeleteView):
    model = Especie
    success_url = reverse_lazy('especie-list')
    template_name = 'core/especie/especie_confirm_delete.html'

######################################################################
# Item Views
######################################################################

class ItemListView(ListView):
  model = Item
  template_name = 'core/item/item_list.html'

class ItemDetailView(DetailView):
  model = Item
  template_name = 'core/item/item_detail.html'

class ItemCreateView(CreateView):
  model = Item
  fields = ['nome', 'categoria', 'preco_unitario', 'dataValidade']
  success_url = reverse_lazy('item-list')
  template_name = 'core/item/item_form.html'

class ItemUpdateView(UpdateView):
  model = Item
  fields = ['preco_unitario']
  success_url = reverse_lazy('item-list')
  template_name = 'core/item/item_form.html'

class ItemDeleteView(DeleteView):
  model = Item
  success_url = reverse_lazy('item-list')
  template_name = 'core/item/item_confirm_delete.html'
  
######################################################################
# Cidade Views
######################################################################

class CidadeListView(ListView):
  model = Cidade
  template_name = 'core/cidade/cidade_list.html'

class CidadeDetailView(DetailView):
  model = Cidade
  template_name = 'core/cidade/cidade_detail.html'

class CidadeCreateView(CreateView):
  model = Cidade
  fields = ['nome', 'uf']
  success_url = reverse_lazy('cidade-list')
  template_name = 'core/cidade/cidade_form.html'

class CidadeUpdateView(UpdateView):
  model = Cidade
  fields = ['nome', 'uf']
  success_url = reverse_lazy('cidade-list')
  template_name = 'core/cidade/cidade_form.html'

class CidadeDeleteView(DeleteView):
  model = Cidade
  success_url = reverse_lazy('cidade-list')
  template_name = 'core/cidade/cidade_confirm_delete.html'

######################################################################
# Endereco Views
######################################################################

class EnderecoListView(ListView):
  model = Endereco
  template_name = 'core/endereco/endereco_list.html'

class EnderecoDetailView(DetailView):
  model = Endereco
  template_name = 'core/endereco/endereco_detail.html'

class EnderecoCreateView(CreateView):
  model = Endereco
  fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'ponto_de_referencia', 'cidade']
  success_url = reverse_lazy('endereco-list')
  template_name = 'core/endereco/endereco_form.html'

class EnderecoUpdateView(UpdateView):
  model = Endereco
  fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'ponto_de_referencia', 'cidade']
  success_url = reverse_lazy('endereco-list')
  template_name = 'core/endereco/endereco_form.html'

class EnderecoDeleteView(DeleteView):
  model = Endereco
  success_url = reverse_lazy('endereco-list')
  template_name = 'core/endereco/endereco_confirm_delete.html'

######################################################################
# Abrigo Views
######################################################################

class AbrigoListView(ListView):
  model = Abrigo
  template_name = 'core/abrigo/abrigo_list.html'

class AbrigoDetailView(DetailView):
  model = Abrigo
  template_name = 'core/abrigo/abrigo_detail.html'

class AbrigoCreateView(CreateView):
  model = Abrigo
  fields = ['nome', 'endereco']
  success_url = reverse_lazy('abrigo-list')
  template_name = 'core/abrigo/abrigo_form.html'

class AbrigoUpdateView(UpdateView):
  model = Abrigo
  fields = ['nome', 'endereco']
  success_url = reverse_lazy('abrigo-list')
  template_name = 'core/abrigo/abrigo_form.html'

class AbrigoDeleteView(DeleteView):
  model = Abrigo
  success_url = reverse_lazy('abrigo-list')
  template_name = 'core/abrigo/abrigo_confirm_delete.html'

######################################################################
# CRMV Views
######################################################################

class CrmvListView(ListView):
  model = CRMV
  template_name = 'core/crmv/crmv_list.html'

class CrmvDetailView(DetailView):
  model = CRMV
  template_name = 'core/crmv/crmv_detail.html'

class CrmvCreateView(CreateView):
  model = CRMV
  fields = ['numero', 'estado']
  success_url = reverse_lazy('crmv-list')
  template_name = 'core/crmv/crmv_form.html'

class CrmvUpdateView(UpdateView):
  model = CRMV
  fields = ['numero', 'estado']
  success_url = reverse_lazy('crmv-list')
  template_name = 'core/crmv/crmv_form.html'

class CrmvDeleteView(DeleteView):
  model = CRMV
  success_url = reverse_lazy('crmv-list')
  template_name = 'core/crmv/crmv_confirm_delete.html'

######################################################################
# TipoConsulta Views
######################################################################

class TipoConsultaListView(ListView):
  model = TipoConsulta
  template_name = 'core/tipoconsulta/tipoconsulta_list.html'

class TipoConsultaDetailView(DetailView):
  model = TipoConsulta
  template_name = 'core/tipoconsulta/tipoconsulta_detail.html'

class TipoConsultaCreateView(CreateView):
  model = TipoConsulta
  fields = ['descricao']
  success_url = reverse_lazy('tipoconsulta-list')
  template_name = 'core/tipoconsulta/tipoconsulta_form.html'

class TipoConsultaUpdateView(UpdateView):
  model = TipoConsulta
  fields = ['descricao']
  success_url = reverse_lazy('tipoconsulta-list')
  template_name = 'core/tipoconsulta/tipoconsulta_form.html'

class TipoConsultaDeleteView(DeleteView):
  model = TipoConsulta
  success_url = reverse_lazy('tipoconsulta-list')
  template_name = 'core/tipoconsulta/tipoconsulta_confirm_delete.html'

######################################################################
# AtendimentoVeterinario Views
######################################################################

class AtendimentoVeterinarioListView(ListView):
  model = AtendimentoVeterinario
  template_name = 'core/atendimentoveterinario/atendimentoveterinario_list.html'

class AtendimentoVeterinarioDetailView(DetailView):
  model = AtendimentoVeterinario
  template_name = 'core/atendimentoveterinario/atendimentoveterinario_detail.html'

class AtendimentoVeterinarioCreateView(CreateView):
  model = AtendimentoVeterinario
  fields = ['data_do_atendimento', 'observacoes', 'Veterinario_idVeterinario', 'TipoConsulta_idTipoConsulta', 'Animal_idAnimal']
  success_url = reverse_lazy('atendimentoveterinario-list')
  template_name = 'core/atendimentoveterinario/atendimentoveterinario_form.html'

class AtendimentoVeterinarioUpdateView(UpdateView):
  model = AtendimentoVeterinario
  fields = ['data_do_atendimento', 'observacoes']
  success_url = reverse_lazy('atendimentoveterinario-list')
  template_name = 'core/atendimentoveterinario/atendimentoveterinario_form.html'

class AtendimentoVeterinarioDeleteView(DeleteView):
  model = AtendimentoVeterinario
  success_url = reverse_lazy('atendimentoveterinario-list')
  template_name = 'core/atendimentoveterinario/atendimentoveterinario_confirm_delete.html'