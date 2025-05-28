from django.urls import path

from .views import (
    BookmarkView,
    CategoryView,
    CommentView,
    LikeView,
    NewsAPIRootView,
    PublishedNewsRetrieveView,
    PublishedNewsView,
    NewsCreateAPIView,
    CustomTagList,
    UploadView,
)

urlpatterns = [
    path("", NewsAPIRootView.as_view(), name="api-news"),
    path("newslist/", PublishedNewsView.as_view(), name="newslist-api"),
    path("newslist/create/", NewsCreateAPIView.as_view(), name="newscreate-api"),
    path(
        "newslist/<int:pk>", PublishedNewsRetrieveView.as_view(), name="newsdetail-api"
    ),
    path("upload/", UploadView.as_view(), name="upload-api"),
    path("category/", CategoryView.as_view(), name="category-api"),
    path("tags/", CustomTagList.as_view(), name="tags-api"),
    path("like/", LikeView.as_view(), name="like-api"),
    path("comment/", CommentView.as_view(), name="comment-api"),
    path("bookmark/", BookmarkView.as_view(), name="bookmark-api"),
]
