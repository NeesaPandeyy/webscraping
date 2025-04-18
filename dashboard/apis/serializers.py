from rest_framework import serializers

from dashboard.models import Keyword, StockRecord, Symbol


class StockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRecord
        fields = "__all__"


class SymbolKeywordSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    keyword = serializers.CharField(required=False, allow_blank=True)

    def validate_symbol(self, value):
        if not Symbol.objects.filter(name=value).exists():
            raise serializers.ValidationError("Symbol not found in database")
        return value

    def validate_keyword(self, value):
        if not value:
            return None

        keyword_names = [kw.strip() for kw in value.split(",")]
        keywords = Keyword.objects.filter(keyword__in=keyword_names)

        if not keywords.exists():
            raise serializers.ValidationError("keywords not found in database")
        return value

    def get_symbol_obj(self):
        return Symbol.objects.get(name=self.validated_data["symbol"])

    def get_keyword_qs(self):
        if not self.validated_data.get("keyword"):
            return None
        keyword_names = [kw.strip() for kw in self.validated_data["keyword"].split(",")]
        return Keyword.objects.filter(keyword__in=keyword_names)
