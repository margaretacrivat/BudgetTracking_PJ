import django_filters
from django_filters import DateFilter, CharFilter
from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')
    category = CharFilter(field_name='category', lookup_expr='icontains')
    class Meta:
        model = Expense
        fields = ['category']
        exclude = ['date']





