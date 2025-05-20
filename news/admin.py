from django.contrib import admin
from django.db import models
from mptt.admin import MPTTModelAdmin

from .models import Category, Comment, Like, NewsPost, NewsStatus, Notification


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("name", "parent")
    search_fields = ("name",)
    autocomplete_fields = ("parent",)
    mptt_level_indent = 20


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "status",
        "get_tags",
        "creator",
        "like_count",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "description", "creator__username")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    actions = ["approve_news", "reject_news"]

    def like_count(self, obj):
        return obj.like_set.count()

    like_count.short_description = "Likes"

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    get_tags.short_description = "Tags"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        return qs.filter(models.Q(status=NewsStatus.PUBLISHED) | models.Q(creator=user))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def approve_news(self, request, queryset):
        updated = queryset.update(status=NewsStatus.PUBLISHED)
        self.message_user(request, "Your post has been approved and published")

    approve_news.short_description = "Approve selected news"

    def reject_news(self, request, queryset):
        updated = queryset.update(status=NewsStatus.REJECTED)
        self.message_user(request, "Your post has been rejected")

    reject_news.short_description = "Reject selected news"

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["status"]
        return super().get_readonly_fields(request, obj)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    autocomplete_fields = ("user", "post")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "body", "parent", "created_at")
    search_fields = ("user__username", "post__title", "body")
    list_filter = ("created_at",)
    autocomplete_fields = ("user", "post", "parent")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "actor",
        "verb",
        "target",
        "is_read",
        "created_at",
    )
    list_filter = ("verb", "is_read", "created_at")
    search_fields = ("recipient__username", "actor__username", "target__title")
    autocomplete_fields = ("recipient", "actor", "target")
    ordering = ("-created_at",)
