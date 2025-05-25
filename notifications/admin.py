from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import EmailNotification, Notification


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


@admin.register(EmailNotification)
class EmailNotificationAdmin(ModelAdmin):
    list_display = ("notification", "subject", "sent_at", "status")
    search_fields = ("subject", "body", "status")
    list_filter = ("status", "sent_at")
    readonly_fields = ("sent_at",)
