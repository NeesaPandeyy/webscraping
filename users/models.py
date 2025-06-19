from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimestampAbstractModel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username


class Support(TimestampAbstractModel, models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="support_tickets",
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.subject}"


class PasswordReset(TimestampAbstractModel, models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
