from django.urls import path
from .views import (
   VeterinarioListView, VeterinarioDetailView, VeterinarioCreateView, VeterinarioUpdateView, VeterinarioDeleteView,
   AnimalListView, AnimalDetailView, AnimalCreateView, AnimalUpdateView, AnimalDeleteView,
   EspecieListView, EspecieDetailView, EspecieCreateView, EspecieUpdateView, EspecieDeleteView,
   ItemListView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView,
   CidadeListView, CidadeDetailView, CidadeCreateView, CidadeUpdateView, CidadeDeleteView,
   EnderecoListView, EnderecoDetailView, EnderecoCreateView, EnderecoUpdateView, EnderecoDeleteView,
   AbrigoListView, AbrigoDetailView, AbrigoCreateView, AbrigoUpdateView, AbrigoDeleteView,
   CrmvListView, CrmvDetailView, CrmvCreateView, CrmvUpdateView, CrmvDeleteView,
   TipoConsultaListView, TipoConsultaDetailView, TipoConsultaCreateView, TipoConsultaUpdateView, TipoConsultaDeleteView,
   AtendimentoVeterinarioListView, AtendimentoVeterinarioDetailView, AtendimentoVeterinarioCreateView, AtendimentoVeterinarioUpdateView, AtendimentoVeterinarioDeleteView,
)

urlpatterns = [
   # Veterinario
   path('veterinarios/', VeterinarioListView.as_view(), name='veterinario-list'),
   path('veterinario/<int:pk>/', VeterinarioDetailView.as_view(), name='veterinario-detail'),
   path('veterinario/add/', VeterinarioCreateView.as_view(), name='veterinario-create'),
   path('veterinario/<int:pk>/edit/', VeterinarioUpdateView.as_view(), name='veterinario-update'),
   path('veterinario/<int:pk>/delete/', VeterinarioDeleteView.as_view(), name='veterinario-delete'),

   # Animal
   path('animais/', AnimalListView.as_view(), name='animal-list'),
   path('animal/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
   path('animal/add/', AnimalCreateView.as_view(), name='animal-create'),
   path('animal/<int:pk>/edit/', AnimalUpdateView.as_view(), name='animal-update'),
   path('animal/<int:pk>/delete/', AnimalDeleteView.as_view(), name='animal-delete'),
   
   # Especie
   path('especies/', EspecieListView.as_view(), name='especie-list'),
   path('especie/<int:pk>/', EspecieDetailView.as_view(), name='especie-detail'),
   path('especie/add/', EspecieCreateView.as_view(), name='especie-create'),
   path('especie/<int:pk>/edit/', EspecieUpdateView.as_view(), name='especie-update'),
   path('especie/<int:pk>/delete/', EspecieDeleteView.as_view(), name='especie-delete'),

   # Item
   path('itens/', ItemListView.as_view(), name='item-list'),
   path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
   path('item/add/', ItemCreateView.as_view(), name='item-create'),
   path('item/<int:pk>/edit/', ItemUpdateView.as_view(), name='item-update'),
   path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),

   # Cidade
   path('cidades/', CidadeListView.as_view(), name='cidade-list'),
   path('cidade/<int:pk>/', CidadeDetailView.as_view(), name='cidade-detail'),
   path('cidade/add/', CidadeCreateView.as_view(), name='cidade-create'),
   path('cidade/<int:pk>/edit/', CidadeUpdateView.as_view(), name='cidade-update'),
   path('cidade/<int:pk>/delete/', CidadeDeleteView.as_view(), name='cidade-delete'),

   # Endereço
   path('enderecos/', EnderecoListView.as_view(), name='endereco-list'),
   path('endereco/<int:pk>/', EnderecoDetailView.as_view(), name='endereco-detail'),
   path('endereco/add/', EnderecoCreateView.as_view(), name='endereco-create'),
   path('endereco/<int:pk>/edit/', EnderecoUpdateView.as_view(), name='endereco-update'),
   path('endereco/<int:pk>/delete/', EnderecoDeleteView.as_view(), name='endereco-delete'),

   # Abrigo
   path('abrigos/', AbrigoListView.as_view(), name='abrigo-list'),
   path('abrigo/<int:pk>/', AbrigoDetailView.as_view(), name='abrigo-detail'),
   path('abrigo/add/', AbrigoCreateView.as_view(), name='abrigo-create'),
   path('abrigo/<int:pk>/edit/', AbrigoUpdateView.as_view(), name='abrigo-update'),
   path('abrigo/<int:pk>/delete/', AbrigoDeleteView.as_view(), name='abrigo-delete'),

   # CRMV
   path('crmvs/', CrmvListView.as_view(), name='crmv-list'),
   path('crmv/<int:pk>/', CrmvDetailView.as_view(), name='crmv-detail'),
   path('crmv/add/', CrmvCreateView.as_view(), name='crmv-create'),
   path('crmv/<int:pk>/edit/', CrmvUpdateView.as_view(), name='crmv-update'),
   path('crmv/<int:pk>/delete/', CrmvDeleteView.as_view(), name='crmv-delete'),
   
   # Tipo de Consulta
   path('tiposconsulta/', TipoConsultaListView.as_view(), name='tipoconsulta-list'),
   path('tipoconsulta/<int:pk>/', TipoConsultaDetailView.as_view(), name='tipoconsulta-detail'),
   path('tipoconsulta/add/', TipoConsultaCreateView.as_view(), name='tipoconsulta-create'),
   path('tipoconsulta/<int:pk>/edit/', TipoConsultaUpdateView.as_view(), name='tipoconsulta-update'),
   path('tipoconsulta/<int:pk>/delete/', TipoConsultaDeleteView.as_view(), name='tipoconsulta-delete'),
   
   # Atendimento Veterinário
   path('atendimentos/', AtendimentoVeterinarioListView.as_view(), name='atendimentoveterinario-list'),
   path('atendimento/<int:pk>/', AtendimentoVeterinarioDetailView.as_view(), name='atendimentoveterinario-detail'),
   path('atendimento/add/', AtendimentoVeterinarioCreateView.as_view(), name='atendimentoveterinario-create'),
   path('atendimento/<int:pk>/edit/', AtendimentoVeterinarioUpdateView.as_view(), name='atendimentoveterinario-update'),
   path('atendimento/<int:pk>/delete/', AtendimentoVeterinarioDeleteView.as_view(), name='atendimentoveterinario-delete'),
]