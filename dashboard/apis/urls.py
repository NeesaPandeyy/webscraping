from django.urls import path

from .views import SentimentListAPIView, StockListAPIView

urlpatterns = [
    path("", StockListAPIView.as_view(), name="stock-api"),
    path("sentiment/", SentimentListAPIView.as_view(), name="sentiment-api"),
]
