import re
from urllib.parse import urljoin

from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from news.models import Bookmark, Category, Comment, Like, NewsPost


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "parent",
            "body",
            "created_at",
        ]


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Like
        fields = [
            "id",
            "user",
            "post",
        ]


class NewsSerializer(TaggitSerializer, serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    # comments = CommentSerializer(many=True, read_only=True)

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
        model = NewsPost
        fields = [
            "id",
            "title",
            "description",
            "tags",
            "likes_count",
            # "comments",
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


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["post", "user", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        validated_data["user"] = request.user
        instance, _ = Bookmark.objects.get_or_create(**validated_data)
        return instance
