from django.urls import path

from .views import AccountsAPIRootView, LoginView, RegisterView, UserListView

urlpatterns = [
    path("", AccountsAPIRootView.as_view(), name="api-accounts"),
    path("userlist/", UserListView.as_view(), name="user-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
