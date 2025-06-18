from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import CustomUser, Support


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "bio", "profile_picture"]


class RegistersSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def validate_username(self, data):
        if CustomUser.objects.filter(username=data).exists():
            raise serializers.ValidationError("Username already exists.")
        return data

    def validate_email(self, data):
        if CustomUser.objects.filter(email=data).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        return user


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ["id", "user", "subject", "message", "created_at"]
        read_only_fields = ["user", "created_at"]
