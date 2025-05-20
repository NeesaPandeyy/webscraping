from django.db.models import Q
from django_filters import rest_framework as filters

from news.models import Category


class CustomFilter(filters.CharFilter):
    def filter(self, queryset, value):
        values = [v.strip() for v in value.split(",") if v.strip()]
        if not value:
            return queryset

        query = Q()
        for val in values:
            lookup = f"{self.field_name}__icontains"
            query |= Q(**{lookup: val})
        return queryset.filter(query)


class NewsFilter(filters.FilterSet):
    catogory = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category",
        label="Category",
    )
    tags = CustomFilter(
        field_name="tags__name",
        lookup_expr="icontains",
        label="Tags",
    )
