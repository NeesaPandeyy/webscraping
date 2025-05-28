from django.urls import path

from .views import NotificationAPIRootView, NotificationListView, ReadNotificationView

urlpatterns = [
    path("", NotificationAPIRootView.as_view(), name="api-notification"),
    path("notify/", NotificationListView.as_view(), name="notification-api"),
    path(
        "notify/<int:pk>/", ReadNotificationView.as_view(), name="readnotification-api"
    ),
]
