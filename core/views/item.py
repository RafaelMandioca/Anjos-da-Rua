# core/views/item.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from ..models import Item
from ..forms.form_item import ItemForm
from .cadastros_gerais import generic_create_update_view

# --- Item Views ---
class ItemListView(ListView): 
    model = Item
    template_name = 'core/item/item_list.html'

class ItemDetailView(DetailView): 
    model = Item
    template_name = 'core/item/item_detail.html'

class ItemDeleteView(DeleteView): 
    model = Item
    success_url = reverse_lazy('item-list')
    template_name = 'core/item/item_confirm_delete.html'

def item_create(request):
    # Corrigindo o caminho do template para o formulário
    return generic_create_update_view(request, ItemForm, 'Item', 'core/item/item_form.html', 'item-list')

def item_update(request, pk):
    # Corrigindo o caminho do template para o formulário
    return generic_create_update_view(request, ItemForm, 'Item', 'core/item/item_form.html', 'item-list', pk=pk)