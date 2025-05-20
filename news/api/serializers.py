import re
from urllib.parse import urljoin

from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from news.models import Category, Comment, NewsPost, Notification


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


class NewsSerializer(TaggitSerializer, serializers.ModelSerializer):
    like = serializers.IntegerField(source="like_set.count", read_only=True)
    description = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)

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
            "like",
            "comments",
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


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_title = serializers.CharField(source='target.title', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'notif_type',
            'actor_username',
            'target_title',
            'created_at',
            'is_read',
        ]