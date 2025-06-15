from django.urls import path

from .views import (AnnouncementListAPIView, ScraperAPIRootView,
                    SentimentListAPIView, StockListAPIView, SymbolListAPIView)

urlpatterns = [
    path("", ScraperAPIRootView.as_view(), name="api-scraper"),
    path("news/", StockListAPIView.as_view(), name="stock-api"),
    path("symbols/", SymbolListAPIView.as_view(), name="symbol-list"),
    path("sentiment/", SentimentListAPIView.as_view(), name="sentiment-api"),
    path("announcement/", AnnouncementListAPIView.as_view(), name="announcement-api"),
]
