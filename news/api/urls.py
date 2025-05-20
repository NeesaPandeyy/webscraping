from django.urls import path

from .views import (CategoryView, CommentView, NewsAPIRootView,
                    NotificationListView, PublishedNewsView)

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="api-news"),
    path("newslist/", PublishedNewsView.as_view(), name="newslist-api"),
    path("category/", CategoryView.as_view(), name="category-api"),
    path("comment/", CommentView.as_view(), name="comment-api"),
    path("notification/", NotificationListView.as_view(), name="notification-api"),
]
