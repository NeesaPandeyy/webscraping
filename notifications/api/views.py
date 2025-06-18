from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination
from notifications.models import Notification

from .serializers import NotificationSerializer


class NotificationAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        return Response(
            {
                "notify": reverse("notification-api", request=request, format=format),
            }
        )


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=["Notifications"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by(
            "-created_at"
        )


class ReadNotificationView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=["Notifications"],
    )
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)

        if not notification.is_read:
            notification.is_read = True
            notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
