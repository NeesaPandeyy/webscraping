import json

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from dashboard.apis.filters import StockRecordFilter
from dashboard.models import StockRecord, Symbol
from scraper.services import apply_sentiment

from .serializers import (SentimentSerializer, StockRecordSerializer,
                          SymbolSerializer)


class CustomPagination(PageNumberPagination):
    page_size = 10


class SymbolListAPIView(generics.ListAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer


class StockListAPIView(generics.ListAPIView):
    queryset = StockRecord.objects.all()
    serializer_class = StockRecordSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter


class SentimentListAPIView(generics.ListAPIView):
    serializer_class = SentimentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter
    pagination_class = CustomPagination
    queryset = StockRecord.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        result_json = apply_sentiment(queryset)
        result = json.loads(result_json)

        page = self.paginate_queryset(result)
        return self.get_paginated_response(page)
