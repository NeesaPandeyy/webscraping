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
from core.permissions import IsOwnerOrReadOnly
from news.api.filters import NewsFilter
from news.models import Bookmark, Category, Comment, CustomTag, Like, NewsPost

from .serializers import (
    BookmarkSerializer,
    BookmarkToggleSerializer,
    CategorySerializer,
    CommentSerializer,
    CustomTagSerializer,
    LikeToggleSerializer,
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
                "like": reverse(
                    "like-api", kwargs={"post_id": 1}, request=request, format=format
                ),
                "comment": reverse(
                    "comment-api", kwargs={"post_id": 1}, request=request, format=format
                ),
                "mybookmark": reverse("bookmark-api", request=request, format=format),
                "bookmark": reverse(
                    "bookmark-toggle",
                    kwargs={"post_id": 1},
                    request=request,
                    format=format,
                ),
            }
        )


class NewsCreateAPIView(generics.CreateAPIView):
    queryset = NewsPost.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Custom News"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Custom News"],
    )
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PublishedNewsView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer

    @swagger_auto_schema(
        operation_summary="List Published News",
        tags=["Custom News"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return NewsPost.objects.filter(status__in=["published"]).order_by("-created_at")


class PublishedNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = NewsPost.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(tags=["Custom News"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Custom News"])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Custom News"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Custom News"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Like"],
        manual_parameters=[
            openapi.Parameter(
                "post_id",
                openapi.IN_PATH,
                description="ID of the post to like/unlike",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: LikeToggleSerializer},
    )
    def post(self, request, post_id):
        post = get_object_or_404(NewsPost, id=post_id)
        liked = Like.objects.toggle_like(request.user, post)
        return Response({"liked": liked})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return (
            Comment.objects.filter(post_id=post_id, parent=None)
            .select_related("user")
            .prefetch_related("replies")
        )

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(user=self.request.user, post_id=post_id)

    @swagger_auto_schema(tags=["Comments"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Comments"])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(tags=["Comments"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Comments"])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Comments"])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Comments"])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BookmarkToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Bookmark"],
        manual_parameters=[
            openapi.Parameter(
                "post_id",
                openapi.IN_PATH,
                description="ID of the post to bookmark/unbookmark",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: BookmarkToggleSerializer},
    )
    def post(self, request, post_id):
        post = get_object_or_404(NewsPost, id=post_id)
        bookmarked = Bookmark.objects.toggle_bookmark(request.user, post)
        return Response({"bookmarked": bookmarked})


class BookmarkView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Bookmark"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=["Categories"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
