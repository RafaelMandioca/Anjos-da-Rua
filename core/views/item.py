# core/views/item.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from ..models import Item
from ..forms.form_item import ItemForm
from .cadastros_gerais import generic_create_update_view

# --- Item Views ---
class ItemListView(ListView): model = Item
class ItemDetailView(DetailView): model = Item
class ItemDeleteView(DeleteView): model = Item; success_url = reverse_lazy('item-list')

def item_create(request):
    return generic_create_update_view(request, ItemForm, 'Item', 'core/basic_form.html', 'item-list')

def item_update(request, pk):
    return generic_create_update_view(request, ItemForm, 'Item', 'core/basic_form.html', 'item-list', pk=pk)
