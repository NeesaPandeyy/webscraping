from django.urls import path

from .views import SentimentListAPIView, StockListAPIView, SymbolListAPIView

urlpatterns = [
    path("news/", StockListAPIView.as_view(), name="stock-api"),
    path("symbols/", SymbolListAPIView.as_view(), name="symbol-list"),
    path("sentiment/", SentimentListAPIView.as_view(), name="sentiment-api"),
]
