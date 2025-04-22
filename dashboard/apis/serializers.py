from rest_framework import serializers

from dashboard.models import StockRecord, Symbol


class SymbolSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source="sector.sector", read_only=True)

    class Meta:
        model = Symbol
        fields = ["name", "sector_name"]


class StockRecordSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()

    class Meta:
        model = StockRecord
        fields = ["id", "symbol", "title", "summary", "url", "date"]


class SentimentSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=False)
    sector_type = serializers.CharField(source="symbol.sector.sector", read_only=True)

    def validate_symbol(self, value):
        if not Symbol.objects.filter(name=value).exists():
            raise serializers.ValidationError("Symbol not found in database")
        return value

    def get_symbol_obj(self):
        return Symbol.objects.get(name=self.validated_data["symbol"])
