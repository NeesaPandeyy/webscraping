from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from news.api.filters import NewsFilter
from news.models import Category, News

from .serializers import CategorySerializer, NewsSerializer


class NewsAPIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "category": reverse("category-api", request=request, format=format),
                "newslist": reverse("newslist-api", request=request, format=format),
            }
        )


class PublishedNewsView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
    # permission_classes = [IsAdminUser]
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(status__in=["published"])


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
