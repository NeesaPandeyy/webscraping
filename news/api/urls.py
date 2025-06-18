from django.urls import path

from .views import (
    BookmarkView,
    CategoryView,
    CommentDetailView,
    CommentListCreateView,
    CustomTagList,
    LikeView,
    NewsAPIRootView,
    NewsCreateAPIView,
    PublishedNewsDetailView,
    PublishedNewsView,
)

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="api-news"),
    path("news/", PublishedNewsView.as_view(), name="newslist-api"),
    path("news/create/", NewsCreateAPIView.as_view(), name="newscreate-api"),
    path("news/<int:pk>/", PublishedNewsDetailView.as_view(), name="newsdetail-api"),
    path("category/", CategoryView.as_view(), name="category-api"),
    path("tags/", CustomTagList.as_view(), name="tags-api"),
    path("like/", LikeView.as_view(), name="like-api"),
    path(
        "news/<int:post_id>/comments/",
        CommentListCreateView.as_view(),
        name="comment-api",
    ),
    path(
        "news/<int:post_id>/comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail-api",
    ),
    path("bookmark/", BookmarkView.as_view(), name="bookmark-api"),
]
