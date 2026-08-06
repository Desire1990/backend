import django_filters
from django.db.models import F
from .models import Medicine

class MedicineFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='lte')
    min_cost = django_filters.NumberFilter(field_name='cost_price', lookup_expr='gte')
    max_cost = django_filters.NumberFilter(field_name='cost_price', lookup_expr='lte')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')

    class Meta:
        model = Medicine
        fields = ['category', 'brand', 'batch_number']

    def filter_low_stock(self, queryset, name, value):
        if value:
            return queryset.filter(quantity__lte=F('reorder_level'))
        return queryset