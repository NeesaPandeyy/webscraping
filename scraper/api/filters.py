from django import forms
from django.db.models import Q
from django_filters import rest_framework as filters

from scraper.models import Keyword, Sector, StockRecord, Symbol


class CustomFilter(filters.CharFilter):
    def filter(self, queryset, value):
        values = [v.strip() for v in value.split(",") if v.strip()]
        if not value:
            return queryset

        query = Q()
        for val in values:
            query |= Q(tags__icontains=val)
        return queryset.filter(query)


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
    date = filters.DateFilter(
        field_name="date",
        lookup_expr="exact",
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"}),
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
    # title = CustomFilter(
    #     field_name="title",
    #     lookup_expr="icontains",
    #     label="title",
    # )
    keyword = filters.ModelChoiceFilter(
        queryset=Keyword.objects.all(),
        method="filter_with_keyword",
        field_name="name",
        label="Keyword",
    )

    def filter_with_keyword(self, queryset, name, value):
        matched_news = queryset.filter(
            Q(title__icontains=value.name) | Q(summary__icontains=value.name)
        )
        return matched_news

    class Meta:
        model = StockRecord
        fields = ["symbol", "date", "date_after", "date_before", "keyword"]


class AnnouncementFilter(filters.FilterSet):
    tags = CustomFilter(
        field_name="tags",
        lookup_expr="icontains",
        label="tags",
    )
