from django import forms
from django_filters import rest_framework as filters
from dashboard.models import StockRecord


class StockRecordFilter(filters.FilterSet):
    symbol = filters.CharFilter(
        field_name="symbol__name", lookup_expr="icontains", label="Symbol"
    )
    date_after = filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="From Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_before = filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="To Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = StockRecord
        fields = ["symbol", "date_after", "date_before"]
