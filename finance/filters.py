import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['category', 'min_amount', 'max_amount', 'start_date', 'end_date']
