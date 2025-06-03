from django import forms
from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from mptt.admin import DraggableMPTTAdmin
from unfold.admin import ModelAdmin

from .models import Bookmark, Category, Comment, CustomTag, Like, NewsPost


class NewsPostAdminForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = "__all__"
        widgets = {
            "description": CKEditor5Widget(config_name="extends"),
        }

    class Media:
        js = [
            "/static/js/ckeditor5-upload-adapter.js",
        ]


@admin.register(CustomTag)
class CustomTagAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, ModelAdmin):
    mptt_level_indent = 20

    list_display = (
        "tree_actions",
        "indented_title",
        "name",
        "parent",
    )
    list_display_links = ("indented_title",)

    list_filter = ("parent",)
    search_fields = ("name",)
    autocomplete_fields = ("parent",)

    def indented_title(self, obj):
        return obj.name

    indented_title.short_description = "Category"


@admin.register(NewsPost)
class NewsPostAdmin(ModelAdmin):
    form = NewsPostAdminForm
    list_display = (
        "title",
        "category",
        "status",
        "get_tags",
        "creator",
        "likes_count",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "description", "creator__username")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    actions = ["approve_news", "reject_news"]

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    get_tags.short_description = "Tags"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        return qs.filter(models.Q(status=self.PUBLISHED) | models.Q(creator=user))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def approve_news(self, request, queryset):
        updated = queryset.update(status=self.PUBLISHED)
        self.message_user(request, "Your post has been approved and published")

    approve_news.short_description = "Approve selected news"

    def reject_news(self, request, queryset):
        updated = queryset.update(status=self.REJECTED)
        self.message_user(request, "Your post has been rejected")

    reject_news.short_description = "Reject selected news"

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["status"]
        return super().get_readonly_fields(request, obj)


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    autocomplete_fields = ("user", "post")
    list_filter = ("user", "post")


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin, ModelAdmin):
    mptt_level_indent = 20

    list_display = (
        "tree_actions",
        "indented_title",
        "user",
        "post",
        "parent",
        "created_at",
    )
    list_display_links = ("indented_title",)

    list_filter = ("post", "user")
    search_fields = ("body", "user__username")

    field_layout = (
        (
            "Comment Info",
            {
                "fields": ("user", "post", "body", "parent"),
            },
        ),
    )


@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin):
    list_display = ("user", "post", "created_at")
    search_fields = ("user__username", "post__title")
    autocomplete_fields = ("user", "post")
    list_filter = ("user", "post")
