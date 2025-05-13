import json

from django.templatetags.static import static
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination
from scraper.api.filters import AnnouncementFilter, StockRecordFilter
from scraper.documents import StockRecordDocument
from scraper.models import Announcement, StockRecord, Symbol
from scraper.services import SentimentAnalysis

from .serializers import (AnnouncementSerializer, SentimentSerializer,
                          StockRecordSerializer, SymbolSerializer)


class ScraperAPIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "news": reverse("stock-api", request=request, format=format),
                "symbols": reverse("symbol-list", request=request, format=format),
                "sentiment": reverse("sentiment-api", request=request, format=format),
                "announcement": reverse(
                    "announcement-api", request=request, format=format
                ),
            }
        )


class SymbolListAPIView(generics.ListAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer


class StockListAPIView(generics.ListAPIView):
    queryset = StockRecord.objects.all()
    serializer_class = StockRecordSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            search = StockRecordDocument.search().query(
                "multi_match", query=query, fields=["title", "summary", "symbol"]
            )
            results = search[:100]
            ids = [hit.meta.id for hit in results]
            return StockRecord.objects.filter(id__in=ids)
        return StockRecord.objects.all()


class SentimentListAPIView(generics.ListAPIView):
    serializer_class = SentimentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StockRecordFilter
    pagination_class = CustomPagination
    queryset = StockRecord.objects.all()
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        result_json = SentimentAnalysis.apply_sentiment(queryset)
        result = json.loads(result_json)

        chart_url = request.build_absolute_uri(static("scraper/plotchart.png"))

        page = self.paginate_queryset(result)
        paginated_data = self.get_paginated_response(page).data
        paginated_data["chart_url"] = chart_url

        return Response(paginated_data)


class AnnouncementListAPIView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AnnouncementFilter
