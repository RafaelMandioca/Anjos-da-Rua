# core/views/mixins.py

class SortableListViewMixin:
    """
    Adiciona a capacidade de ordenar um ListView a partir de parâmetros na URL.
    Ex: ?sort=nome&direction=asc
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort')
        direction = self.request.GET.get('direction')

        if sort_by:
            order = f"{'-' if direction == 'desc' else ''}{sort_by}"
            queryset = queryset.order_by(order)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort')
        context['current_direction'] = self.request.GET.get('direction')
        return context