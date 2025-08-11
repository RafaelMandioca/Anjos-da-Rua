# core/urls.py

from django.urls import path
from .views import animal, atendimento, cadastros_gerais, item, veterinario

urlpatterns = [
   path('gerenciamento/', cadastros_gerais.gerenciamento, name='gerenciamento'),
   path('abrigo/<int:abrigo_id>/animais/', animal.AnimalPorAbrigoListView.as_view(), name='animais-por-abrigo'),

   # URLs do Perfil
   path('perfil/', veterinario.perfil_view, name='perfil'),
   path('perfil/endereco/', veterinario.perfil_alterar_endereco, name='perfil_alterar_endereco'),
   path('perfil/informacoes/', veterinario.perfil_alterar_informacoes, name='perfil_alterar_informacoes'),
   path('perfil/senha/', veterinario.perfil_alterar_senha, name='perfil_alterar_senha'),
   path('perfil/apagar/', veterinario.PerfilDeleteView.as_view(), name='perfil_apagar_conta'),

   # Veterinario
   path('veterinarios/', veterinario.VeterinarioListView.as_view(), name='veterinario-list'),
   path('veterinario/<int:pk>/', veterinario.VeterinarioDetailView.as_view(), name='veterinario-detail'),
   path('veterinario/add/', veterinario.veterinario_create, name='veterinario-create'),
   path('veterinario/<int:pk>/edit/', veterinario.veterinario_update, name='veterinario-update'),
   path('veterinario/<int:pk>/delete/', veterinario.VeterinarioDeleteView.as_view(), name='veterinario-delete'),

   # Animal (e Especie aninhada)
   path('animais/', animal.AnimalListView.as_view(), name='animal-list'),
   path('animal/<int:pk>/', animal.AnimalDetailView.as_view(), name='animal-detail'),
   path('animal/add/', animal.animal_create_update, name='animal-create'),
   path('animal/<int:pk>/edit/', animal.animal_create_update, name='animal-update'),
   path('animal/<int:pk>/delete/', animal.AnimalDeleteView.as_view(), name='animal-delete'),

   # Item
   path('itens/', item.ItemListView.as_view(), name='item-list'),
   path('item/<int:pk>/', item.ItemDetailView.as_view(), name='item-detail'),
   path('item/add/', item.item_create, name='item-create'),
   path('item/<int:pk>/edit/', item.item_update, name='item-update'),
   path('item/<int:pk>/delete/', item.ItemDeleteView.as_view(), name='item-delete'),

   # Abrigo (e Endereco aninhado)
   path('abrigos/', cadastros_gerais.AbrigoListView.as_view(), name='abrigo-list'),
   path('abrigo/<int:pk>/', cadastros_gerais.AbrigoDetailView.as_view(), name='abrigo-detail'),
   path('abrigo/add/', cadastros_gerais.abrigo_create_update, name='abrigo-create'),
   path('abrigo/<int:pk>/edit/', cadastros_gerais.abrigo_create_update, name='abrigo-update'),
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
   path('animal/<int:animal_id>/atendimentos/', atendimento.AtendimentoPorAnimalListView.as_view(), name='atendimentos-por-animal'),
   path('atendimento/<int:pk>/', atendimento.AtendimentoVeterinarioDetailView.as_view(), name='atendimentoveterinario-detail'),
   path('atendimento/add/', atendimento.atendimento_veterinario_create_update, name='atendimentoveterinario-create'),
   path('atendimento/<int:pk>/edit/', atendimento.atendimento_veterinario_create_update, name='atendimentoveterinario-update'),
   path('atendimento/<int:pk>/delete/', atendimento.AtendimentoVeterinarioDeleteView.as_view(), name='atendimentoveterinario-delete'),
]