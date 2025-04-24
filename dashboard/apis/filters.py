from django import forms
from django_filters import rest_framework as filters

from dashboard.models import Sector, StockRecord, Symbol


class StockRecordFilter(filters.FilterSet):
    symbol = filters.ModelChoiceFilter(
        queryset=Symbol.objects.all(), 
        field_name="symbol", 
        label="Symbol",
    )

    sector = filters.ModelChoiceFilter(
        queryset=Sector.objects.all(),
        field_name="symbol__sector__sector",
        label="Sector",
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
