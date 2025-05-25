from django.conf import settings
from django.db import models

from core.models import TimestampAbstractModel
from news.models import NewsPost


class Notification(TimestampAbstractModel, models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    verb = models.CharField(max_length=255)
    target = models.ForeignKey(
        NewsPost, on_delete=models.CASCADE, null=True, blank=True
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.verb
