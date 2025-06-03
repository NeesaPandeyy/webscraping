from django.urls import path

from .views import create_news_view, published_news_view

urlpatterns = [
    path("create/", create_news_view, name="news-create"),
    path("", published_news_view, name="news-list"),
]
