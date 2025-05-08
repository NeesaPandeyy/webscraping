from django.conf import settings
from rest_framework import serializers

from scraper.models import Announcement, News, StockRecord, Symbol


class SymbolSerializer(serializers.ModelSerializer):
    sector_type = serializers.CharField(source="sector.sector", read_only=True)

    class Meta:
        model = Symbol
        fields = ["name", "sector_type"]


class StockRecordSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()

    class Meta:
        model = StockRecord
        fields = ["id", "symbol", "title", "summary", "url", "date"]


class SentimentSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=False)
    sector_type = serializers.CharField(source="symbol.sector.sector", read_only=True)
    image_url = serializers.SerializerMethodField("get_image_url")

    def validate_symbol(self, value):
        if not Symbol.objects.filter(name=value).exists():
            raise serializers.ValidationError("Symbol not found in database")
        return value

    def get_symbol_obj(self):
        return Symbol.objects.get(name=self.validated_data["symbol"])

    def get_image_url(self, obj):
        if obj.image:
            return settings.MEDIA_URL + str(obj.image)
        return None


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            "title",
            "description",
            "category",
            "slug",
            "created_at",
            "updated_at",
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"
