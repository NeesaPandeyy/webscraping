import os

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser, PasswordReset, Support

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegistersSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
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
                "supportadmin": reverse(
                    "supportadmin-api", request=request, format=format
                ),
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
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=SupportSerializer,
        tags=["Support"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SupportListAdminView(generics.ListAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=["Support"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    @swagger_auto_schema(
        tags=["users"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data["email"]
        user = CustomUser.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = f"{os.getenv('PASSWORD_RESET_BASE_URL')}/{token}"

            send_mail(
                subject="Password Reset Request",
                message=f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(
        tags=["users"],
    )
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password != confirm_password:
            return Response({"error": "Password do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = CustomUser.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["new_password"])
            user.save()

            reset_obj.delete()
            return Response({"success": "Password Updated"})
        else:
            return Response({"error": "No user found"}, status=404)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        tags=["users"],
    )
    def put(self, request, id):
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        confirm_password = request.data["confirm_password"]

        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password didnt matched"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not user.check_password(old_password):
            return Response({"error": "Current password is incorrect"}, status=400)
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"success": "password changed successfully"}, status=200)
