# core/views/item.py

from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .mixins import SortableListViewMixin
from ..models import Item
from ..forms.form_item import ItemForm
from .cadastros_gerais import generic_create_update_view, AdminRequiredMixin, is_admin

# --- Item Views ---

class ItemListView(LoginRequiredMixin, SortableListViewMixin, ListView): 
    model = Item
    template_name = 'core/item/item_list.html'

class ItemDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView): 
    model = Item
    template_name = 'core/item/item_detail.html'

class ItemDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView): 
    model = Item
    success_url = reverse_lazy('item-list')
    template_name = 'core/item/item_confirm_delete.html'

@login_required
@user_passes_test(is_admin)
def item_create(request):
    return generic_create_update_view(request, ItemForm, 'Item', 'core/item/item_form.html', 'item-list')

@login_required
@user_passes_test(is_admin)
def item_update(request, pk):
    return generic_create_update_view(request, ItemForm, 'Item', 'core/item/item_form.html', 'item-list', pk=pk)