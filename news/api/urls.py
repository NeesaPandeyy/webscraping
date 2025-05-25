from django.urls import path

from .views import (CategoryView, CommentView, LikeView, NewsAPIRootView,
                    PublishedNewsRetrieveView, PublishedNewsView)

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="api-news"),
    path("newslist/", PublishedNewsView.as_view(), name="newslist-api"),
    path(
        "newslist/<int:pk>", PublishedNewsRetrieveView.as_view(), name="newsdetail-api"
    ),
    path("category/", CategoryView.as_view(), name="category-api"),
    path("like/", LikeView.as_view(), name="like-api"),
    path("comment/", CommentView.as_view(), name="comment-api"),
]
