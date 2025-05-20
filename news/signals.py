from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from news.utils import create_notification

from .models import Comment, Like, NewsPost


@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created:
        create_notification(
            recipient=instance.post.creator,
            actor=instance.user,
            verb="liked your post",
            target=instance.post,
        )


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        if instance.post.creator != instance.user:
            create_notification(
                recipient=instance.post.creator,
                actor=instance.user,
                verb="commented on your post",
                target=instance.post,
            )
        if instance.parent and instance.parent.user != instance.user:
            create_notification(
                recipient=instance.parent.user,
                actor=instance.user,
                verb="replied to your comment",
                target=instance.post,
            )


@receiver(post_save, sender=NewsPost)
def notify_post(sender, instance, created, **kwargs):
    if created and instance.status == "published":
        recipients = User.objects.exclude(id=instance.creator.id)
        for user in recipients:
            create_notification(
                recipient=user,
                actor=instance.creator,
                verb="posted a new post",
                target=instance,
            )
