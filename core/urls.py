# core/urls.py

from django.urls import path

# Import each view module from the views package directly
from .views import animal, atendimento, cadastros_gerais, item, veterinario

urlpatterns = [
   # Veterinario
   path('veterinarios/', veterinario.VeterinarioListView.as_view(), name='veterinario-list'),
   path('veterinario/<int:pk>/', veterinario.VeterinarioDetailView.as_view(), name='veterinario-detail'),
   path('veterinario/add/', veterinario.veterinario_create, name='veterinario-create'),
   path('veterinario/<int:pk>/delete/', veterinario.VeterinarioDeleteView.as_view(), name='veterinario-delete'),

   # Animal
   path('animais/', animal.AnimalListView.as_view(), name='animal-list'),
   path('animal/<int:pk>/', animal.AnimalDetailView.as_view(), name='animal-detail'),
   path('animal/add/', animal.animal_create, name='animal-create'),
   path('animal/<int:pk>/edit/', animal.animal_update, name='animal-update'),
   path('animal/<int:pk>/delete/', animal.AnimalDeleteView.as_view(), name='animal-delete'),

   # Especie (Assuming these are in 'animal.py' or a new 'especie.py')
   path('especies/', animal.EspecieListView.as_view(), name='especie-list'),
   path('especie/<int:pk>/', animal.EspecieDetailView.as_view(), name='especie-detail'),
   path('especie/add/', animal.especie_create, name='especie-create'),
   path('especie/<int:pk>/edit/', animal.especie_update, name='especie-update'),
   path('especie/<int:pk>/delete/', animal.EspecieDeleteView.as_view(), name='especie-delete'),

   # Item
   path('itens/', item.ItemListView.as_view(), name='item-list'),
   path('item/<int:pk>/', item.ItemDetailView.as_view(), name='item-detail'),
   path('item/add/', item.item_create, name='item-create'),
   path('item/<int:pk>/edit/', item.item_update, name='item-update'),
   path('item/<int:pk>/delete/', item.ItemDeleteView.as_view(), name='item-delete'),

   # Cidade
   path('cidades/', cadastros_gerais.CidadeListView.as_view(), name='cidade-list'),
   path('cidade/<int:pk>/', cadastros_gerais.CidadeDetailView.as_view(), name='cidade-detail'),
   path('cidade/add/', cadastros_gerais.cidade_create, name='cidade-create'),
   path('cidade/<int:pk>/edit/', cadastros_gerais.cidade_update, name='cidade-update'),
   path('cidade/<int:pk>/delete/', cadastros_gerais.CidadeDeleteView.as_view(), name='cidade-delete'),

   # Endereço
   path('enderecos/', cadastros_gerais.EnderecoListView.as_view(), name='endereco-list'),
   path('endereco/<int:pk>/', cadastros_gerais.EnderecoDetailView.as_view(), name='endereco-detail'),
   path('endereco/add/', cadastros_gerais.endereco_create, name='endereco-create'),
   path('endereco/<int:pk>/edit/', cadastros_gerais.endereco_update, name='endereco-update'),
   path('endereco/<int:pk>/delete/', cadastros_gerais.EnderecoDeleteView.as_view(), name='endereco-delete'),

   # Abrigo
   path('abrigos/', cadastros_gerais.AbrigoListView.as_view(), name='abrigo-list'),
   path('abrigo/<int:pk>/', cadastros_gerais.AbrigoDetailView.as_view(), name='abrigo-detail'),
   path('abrigo/add/', cadastros_gerais.abrigo_create, name='abrigo-create'),
   path('abrigo/<int:pk>/edit/', cadastros_gerais.abrigo_update, name='abrigo-update'),
   path('abrigo/<int:pk>/delete/', cadastros_gerais.AbrigoDeleteView.as_view(), name='abrigo-delete'),

   # CRMV
   path('crmvs/', veterinario.CrmvListView.as_view(), name='crmv-list'),
   path('crmv/<int:pk>/', veterinario.CrmvDetailView.as_view(), name='crmv-detail'),
   path('crmv/add/', veterinario.crmv_create, name='crmv-create'),
   path('crmv/<int:pk>/edit/', veterinario.crmv_update, name='crmv-update'),
   path('crmv/<int:pk>/delete/', veterinario.CrmvDeleteView.as_view(), name='crmv-delete'),

   # Tipo de Consulta
   path('tiposconsulta/', atendimento.TipoConsultaListView.as_view(), name='tipoconsulta-list'),
   path('tipoconsulta/<int:pk>/', atendimento.TipoConsultaDetailView.as_view(), name='tipoconsulta-detail'),
   path('tipoconsulta/add/', atendimento.tipoconsulta_create, name='tipoconsulta-create'),
   path('tipoconsulta/<int:pk>/edit/', atendimento.tipoconsulta_update, name='tipoconsulta-update'),
   path('tipoconsulta/<int:pk>/delete/', atendimento.TipoConsultaDeleteView.as_view(), name='tipoconsulta-delete'),

   # Atendimento Veterinário
   path('atendimentos/', atendimento.AtendimentoVeterinarioListView.as_view(), name='atendimentoveterinario-list'),
   path('atendimento/<int:pk>/', atendimento.AtendimentoVeterinarioDetailView.as_view(), name='atendimentoveterinario-detail'),
   path('atendimento/add/', atendimento.atendimento_veterinario_create_update, name='atendimentoveterinario-create'),
   path('atendimento/<int:pk>/edit/', atendimento.atendimento_veterinario_create_update, name='atendimentoveterinario-update'),
   path('atendimento/<int:pk>/delete/', atendimento.AtendimentoVeterinarioDeleteView.as_view(), name='atendimentoveterinario-delete'),
]