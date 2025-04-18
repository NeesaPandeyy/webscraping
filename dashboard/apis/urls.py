from django.urls import path
from .views import StockListAPIView, SentimentListAPIView

urlpatterns = [
    path("stock/", StockListAPIView.as_view(), name="stock-api"),
    path("sentiment/", SentimentListAPIView.as_view(), name="sentiment-api"),
]
