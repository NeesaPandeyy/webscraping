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
from news.models import Bookmark, Category, Comment, Like, NewsPost, CustomTag

from .serializers import (
    BookmarkSerializer,
    CategorySerializer,
    CommentSerializer,
    NewsSerializer,
    CustomTagSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.files.storage import default_storage


import os
from django.conf import settings


class NewsAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        return Response(
            {
                "category": reverse("category-api", request=request, format=format),
                "newslist": reverse("newslist-api", request=request, format=format),
                "newscreate": reverse("newscreate-api", request=request, format=format),
                "upload": reverse("upload-api", request=request, format=format),
                "tags": reverse("tags-api", request=request, format=format),
                "like": reverse("like-api", request=request, format=format),
                "comment": reverse("comment-api", request=request, format=format),
                "bookmark": reverse("bookmark-api", request=request, format=format),
            }
        )


class UploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        base_url = request.build_absolute_uri(settings.MEDIA_URL)

        if not os.path.exists(upload_dir):
            return Response({"images": []})

        image_urls = []
        for filename in os.listdir(upload_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                image_urls.append(base_url + "uploads/" + filename)

        return Response({"images": image_urls})

    def post(self, request, *args, **kwargs):
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "No image uploaded."}, status=400)

        file_path = default_storage.save(os.path.join("uploads", image.name), image)
        image_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)

        return Response({"url": image_url}, status=201)


class CustomTagList(generics.ListCreateAPIView):
    queryset = CustomTag.objects.all()
    serializer_class = CustomTagSerializer


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
        return NewsPost.objects.filter(status__in=["published"])


class NewsCreateAPIView(generics.CreateAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PublishedNewsRetrieveView(generics.RetrieveAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    pagination_class = CustomPagination

    # permission_classes = [IsAdminUser]
    serializer_class = NewsSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve Published News",
        tags=["Custom News"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return NewsPost.objects.filter(status__in=["published"])


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


# class LikeView(generics.ListAPIView):
#     # permission_classes = [IsAuthenticated]

#     queryset = Like.objects.filter(is_liked=True)
#     serializer_class = LikeSerializer
#     pagination_class = CustomPagination


class LikeView(APIView):
    # permission_classes = [IsAuthenticated]
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
