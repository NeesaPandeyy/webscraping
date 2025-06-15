from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination

from ..documents import NewsPostIndex, StockRecordIndex
from .serializers import NewsPostIndexSerializer, StockRecordIndexSerializer


class SearchAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None, tags=["Search"])
    def get(self, request, format=None):
        return Response(
            {
                "stockrecord": reverse(
                    "stockrecorddocument-api-list", request=request, format=format
                ),
                "newsrecord": reverse(
                    "newsrecorddocument-api-list", request=request, format=format
                ),
            }
        )


class StockRecordViewset(DocumentViewSet):
    document = StockRecordIndex
    serializer_class = StockRecordIndexSerializer
    filter_backends = [SearchFilterBackend]
    pagination_class = CustomPagination
    lookup_field = "id"
    search_fields = {
        "title": {"fuzziness": "AUTO"},
        "summary": {"fuzziness": "AUTO"},
    }

    @swagger_auto_schema(
        tags=["Search"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class NewsPostViewset(DocumentViewSet):
    document = NewsPostIndex
    serializer_class = NewsPostIndexSerializer
    filter_backends = [SearchFilterBackend]
    pagination_class = CustomPagination
    lookup_field = "id"
    search_fields = {
        "title": {"fuzziness": "AUTO"},
        "description": {"fuzziness": "AUTO"},
    }

    @swagger_auto_schema(
        tags=["Search"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
