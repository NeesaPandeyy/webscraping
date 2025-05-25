from .models import Notification


def create_notification(recipient, actor, verb, target=None):
    if recipient != actor:
        Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target,
        )
