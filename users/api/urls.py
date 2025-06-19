from django.urls import path

from .views import (
    AccountsAPIRootView,
    ChangePasswordView,
    CreateSupportView,
    LoginView,
    ProfileView,
    RegisterView,
    RequestPasswordReset,
    ResetPassword,
    SupportListAdminView,
    UserView,
)

urlpatterns = [
    path("", AccountsAPIRootView.as_view(), name="api-accounts"),
    path("users/", UserView.as_view(), name="users-api"),
    path("register/", RegisterView.as_view(), name="register-api"),
    path("login/", LoginView.as_view(), name="login-api"),
    path("profile/", ProfileView.as_view(), name="profile-api"),
    path(
        "profile/change_password/<int:id>/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "password-reset/request/",
        RequestPasswordReset.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/<str:token>/",
        ResetPassword.as_view(),
        name="password-reset-confirm",
    ),
    path("support/create/", CreateSupportView.as_view(), name="support-api"),
    path("support/admin/", SupportListAdminView.as_view(), name="supportadmin-api"),
]
