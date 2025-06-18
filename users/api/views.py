from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser, Support

from .serializers import (
    LoginSerializer,
    RegistersSerializer,
    SupportSerializer,
    UserSerializer,
)


class AccountsAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        return Response(
            {
                "users": reverse("users-api", request=request, format=format),
                "register": reverse("register-api", request=request, format=format),
                "login": reverse("login-api", request=request, format=format),
                "support": reverse("support-api", request=request, format=format),
                "profile": reverse("profile-api", request=request, format=format),
            }
        )


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        tags=["users"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistersSerializer

    @swagger_auto_schema(
        request_body=RegistersSerializer,
        tags=["users"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        tags=["users"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        tokens = get_tokens(user)
        return Response(
            {"tokens": tokens, "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        tags=["users"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=["users"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=["users"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateSupportView(generics.CreateAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=SupportSerializer,
        responses={201: SupportSerializer},
        tags=["users"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
