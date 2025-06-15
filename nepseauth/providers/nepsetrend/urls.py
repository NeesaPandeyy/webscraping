from django.urls import path

from .views import oauth2_callback, oauth2_login

urlpatterns = [
    path("login/", oauth2_login, name="nepsetrend_login"),
    path("login/callback", oauth2_callback, name="nepsetrend_callback"),
]
