from django_filters import rest_framework as filters

from dashboard.models import StockRecord


class StockRecordFilter(filters.FilterSet):
    symbol = filters.CharFilter(field_name="symbol__name", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = StockRecord
        fields = ["symbol", "title"]
