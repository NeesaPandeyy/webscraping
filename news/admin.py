from django.contrib import admin
from django.db import models
from mptt.admin import MPTTModelAdmin

from .models import Category, Comment, News, NewsStatus


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("name", "parent")
    search_fields = ("name",)
    autocomplete_fields = ("parent",)
    mptt_level_indent = 20


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "slug", "creator", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "description")
    actions = ["approve_news", "reject_news"]
    autocomplete_fields = ["category"]

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


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ("post", "body")
    list_filter = ("created_at",)
