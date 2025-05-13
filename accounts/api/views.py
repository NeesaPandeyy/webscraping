from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .serializers import (LoginSerializer, RegisterSerializer,
                          UserListSerializer)


class AccountsAPIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "user-list": reverse("user-list", request=request, format=format),
                "register": reverse("register", request=request, format=format),
                "login": reverse("login", request=request, format=format),
            }
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # permission_classes = [IsAdminUser]


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"user": serializer.data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
