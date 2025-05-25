from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from .models import CustomUser, Support


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    model = CustomUser

    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("is_superuser",)
    search_fields = ("username", "email")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("bio", "profile_picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


@admin.register(Support)
class SupportTicketAdmin(ModelAdmin):
    list_display = ("subject", "user", "created_at")
    search_fields = ("subject", "message", "user__username")
    list_filter = ("created_at",)
