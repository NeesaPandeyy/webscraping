from bs4 import BeautifulSoup
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from news.models import Bookmark, Category, Comment, CustomTag, NewsPost


class CustomTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTag
        fields = ["name"]


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    replies = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "parent",
            "body",
            "replies",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]


class LikeToggleSerializer(serializers.Serializer):
    liked = serializers.BooleanField()


class NewsSerializer(TaggitSerializer, serializers.ModelSerializer):
    description = serializers.CharField()
    tags = TagListSerializerField(required=False, allow_null=True, allow_empty=True)

    class Meta:
        model = NewsPost
        fields = [
            "id",
            "title",
            "description",
            "tags",
            "likes_count",
            "category",
            "slug",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            soup = BeautifulSoup(data["description"], "html.parser")
            for tag in soup.find_all(["img", "video", "source"]):
                src = tag.get("src")
                if src and src.startswith("/"):
                    full_url = request.build_absolute_uri(src)
                    tag["src"] = full_url
            data["description"] = str(soup)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
        ]


class BookmarkToggleSerializer(serializers.Serializer):
    bookmarked = serializers.BooleanField()


class BookmarkSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "post", "post_title", "created_at"]
