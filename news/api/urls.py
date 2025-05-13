from django.urls import path

from .views import CategoryView, NewsAPIRootView, PublishedNewsView

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="api-news"),
    path("newslist/", PublishedNewsView.as_view(), name="newslist-api"),
    path("category/", CategoryView.as_view(), name="category-api"),
]
