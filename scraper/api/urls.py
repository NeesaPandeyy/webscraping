from django.urls import path

from .views import (AnnouncementListAPIView, NewsListCreateAPIView,
                    NewsRetrieveUpdateDestroyAPIView, SentimentListAPIView,
                    StockListAPIView, SymbolListAPIView)

urlpatterns = [
    path("", StockListAPIView.as_view(), name="stock-api"),
    path("symbols/", SymbolListAPIView.as_view(), name="symbol-list"),
    path("sentiment/", SentimentListAPIView.as_view(), name="sentiment-api"),
    path("news/", NewsListCreateAPIView.as_view(), name="newslist-api"),
    path(
        "news/<int:pk>/",
        NewsRetrieveUpdateDestroyAPIView.as_view(),
        name="newsedit-api",
    ),
    path("announcement/", AnnouncementListAPIView.as_view(), name="announcement-api"),
]
