from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination
from news.api.filters import NewsFilter
from news.models import Bookmark, Category, Comment, CustomTag, Like, NewsPost

from .serializers import (
    BookmarkSerializer,
    CategorySerializer,
    CommentSerializer,
    CustomTagSerializer,
    NewsSerializer,
)


class NewsAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        return Response(
            {
                "category": reverse("category-api", request=request, format=format),
                "newslist": reverse("newslist-api", request=request, format=format),
                "newscreate": reverse("newscreate-api", request=request, format=format),
                "tags": reverse("tags-api", request=request, format=format),
                "like": reverse("like-api", request=request, format=format),
                "comment": reverse("comment-api", request=request, format=format),
                "bookmark": reverse("bookmark-api", request=request, format=format),
            }
        )


class CustomTagList(generics.ListCreateAPIView):
    queryset = CustomTag.objects.all()
    serializer_class = CustomTagSerializer

    @swagger_auto_schema(
        tags=["Tags"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Tags"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PublishedNewsView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer

    @swagger_auto_schema(
        operation_summary="List Published News",
        manual_parameters=[
            openapi.Parameter(
                name="category",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter news posts by category",
            ),
            openapi.Parameter(
                name="tags",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter news posts by tags",
            ),
            openapi.Parameter(
                name="title",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter news posts by title",
            ),
        ],
        tags=["Custom News"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return NewsPost.objects.filter(status__in=["published"]).order_by("-created_at")


class NewsCreateAPIView(generics.CreateAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsSerializer

    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=["Custom News"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PublishedNewsRetrieveView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    queryset = NewsPost.objects.filter(status="published")
    lookup_field = "pk"
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_summary="Retrieve a single published news item",
        tags=["Custom News"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=["Categories"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=["Comments"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Like"],
    )
    def post(self, request, post_id):
        post = get_object_or_404(NewsPost, id=post_id)
        liked = Like.objects.toggle_like(request.user, post)
        return Response({"liked": liked})


class BookmarkView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    pagination_class = CustomPagination
    queryset = Bookmark.objects.all()

    @swagger_auto_schema(
        tags=["Bookmarks"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Bookmarks"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
