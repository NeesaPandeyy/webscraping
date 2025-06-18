from django.urls import path

from .views import (
    AccountsAPIRootView,
    CreateSupportView,
    LoginView,
    ProfileView,
    RegisterView,
    UserView,
    SupportListAdminView,
)

urlpatterns = [
    path("", AccountsAPIRootView.as_view(), name="api-accounts"),
    path("users/", UserView.as_view(), name="users-api"),
    path("register/", RegisterView.as_view(), name="register-api"),
    path("login/", LoginView.as_view(), name="login-api"),
    path("profile/", ProfileView.as_view(), name="profile-api"),
    path("support/create/", CreateSupportView.as_view(), name="support-api"),
    path("support/admin/", SupportListAdminView.as_view(), name="supportadmin-api"),
]
