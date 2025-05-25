import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags

from news.models import Comment, Like, NewsPost
from notifications.utils import create_notification

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="send_welcome_email")
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Welcome!",
            "Thank you for signing up",
            "neesapandey56@gmail.com",
            [instance.email],
            fail_silently=False,
        )


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


@receiver(post_save, sender=NewsPost)
def notify_newpost_mail(sender, instance, created, **kwargs):
    if created and instance.status == "published":
        users = User.objects.exclude(id=instance.creator.id)
        subject = f"New Post:{instance.title}"

        def resize_images(html):
            return re.sub(
                r"<img([^>]+)>", r'<img\1 style="max-width:500px; height:auto;">', html
            )

        resized_description = resize_images(instance.description)

        message = f"""
                <b>{instance.title} </b> \n
                {resized_description}
                        """

        plain_message = strip_tags(message)

        for user in users:
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )

            msg.attach_alternative(message, "text/html")
            msg.send(fail_silently=False)
