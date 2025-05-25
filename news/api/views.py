from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination
from news.api.filters import NewsFilter
from news.models import Category, Comment, Like, NewsPost

from .serializers import (CategorySerializer, CommentSerializer,
                          LikeSerializer, NewsSerializer)


class NewsAPIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "category": reverse("category-api", request=request, format=format),
                "newslist": reverse("newslist-api", request=request, format=format),
                "like": reverse("like-api", request=request, format=format),
                "comment": reverse("comment-api", request=request, format=format),
            }
        )


class PublishedNewsView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    pagination_class = CustomPagination

    # permission_classes = [IsAdminUser]
    serializer_class = NewsSerializer

    def get_queryset(self):
        return NewsPost.objects.filter(status__in=["published"])


class PublishedNewsRetrieveView(generics.RetrieveAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    pagination_class = CustomPagination

    # permission_classes = [IsAdminUser]
    serializer_class = NewsSerializer

    def get_queryset(self):
        return NewsPost.objects.filter(status__in=["published"])


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination


class LikeView(generics.ListAPIView):
    queryset = Like.objects.filter(is_liked=True)
    serializer_class = LikeSerializer
    pagination_class = CustomPagination
