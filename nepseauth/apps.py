from django.apps import AppConfig


class NepseauthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "nepseauth"

    def ready(self):
        import nepseauth.providers.nepsetrend.provider  # noqa F401
