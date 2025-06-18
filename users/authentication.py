from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        header = super().get_header(request)
        if header is None:
            return None

        return b"Bearer " + header if b" " not in header else header
