from django.db import models
from django.contrib.auth.models import User
from news.models import NewsPost

class Notification(models.Model):

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    verb = models.CharField(max_length=255)  
    target = models.ForeignKey(
        NewsPost, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.verb
