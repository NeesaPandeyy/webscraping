import json

from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from dashboard.apis.filters import StockRecordFilter
from dashboard.models import StockRecord
from scraper.services import apply_sentiment

from .serializers import StockRecordSerializer, SymbolKeywordSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10


class StockListAPIView(generics.ListAPIView):
    queryset = StockRecord.objects.all()
    serializer_class = StockRecordSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter


class SentimentListAPIView(generics.ListAPIView):
    serializer_class = SymbolKeywordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        serializer = SymbolKeywordSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        self.symbol_obj = serializer.get_symbol_obj()
        queryset = StockRecord.objects.filter(symbol=self.symbol_obj)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            result_json = apply_sentiment(queryset)
            result = json.loads(result_json)
        except Exception as e:
            return Response({f"error: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        page = self.paginate_queryset(result)
        return self.get_paginated_response(page)
