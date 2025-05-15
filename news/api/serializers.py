import re
from urllib.parse import urljoin

from rest_framework import serializers

from news.models import Category, Comment, News


class NewsSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        request = self.context.get("request")
        if not request:
            return obj.decription

        base_url = request.build_absolute_uri("/")

        return re.sub(
            r'src="(\/media[^\\"]+)"',
            lambda m: f'src="{urljoin(base_url, m.group(1))}',
            obj.description,
        )

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "description",
            "category",
            "slug",
            "created_at",
            "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "parent",
            "body",
            "created_at",
        ]
