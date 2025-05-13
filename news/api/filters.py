from django_filters import rest_framework as filters

from news.models import Category


class NewsFilter(filters.FilterSet):
    catogory = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category",
        label="Category",
    )
