from django.urls import include, path

urlpatterns = [
    path("", include("nepseauth.providers.nepsetrend.urls")),
]
