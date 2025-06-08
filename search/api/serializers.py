from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import NewsPostIndex, StockRecordIndex


class NewsPostIndexSerializer(DocumentSerializer):
    class Meta:
        document = NewsPostIndex
        fields = ("title", "description", "category", "tags")


class StockRecordIndexSerializer(DocumentSerializer):
    class Meta:
        document = StockRecordIndex
        fields = ("title", "summary", "symbol", "keywords")
