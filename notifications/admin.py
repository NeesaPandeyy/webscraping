from django.contrib import admin
from .models import Notification
from unfold.admin import ModelAdmin


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
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
