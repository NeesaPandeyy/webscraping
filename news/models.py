from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey

from core.models import TimestampAbstractModel


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class NewsStatus(models.TextChoices):
    PUBLISHED = "published", "Published"
    DRAFT = "draft", "Draft"
    PENDING_REVIEW = "pending_review", "Pending Review"
    REJECTED = "rejected", "Rejected"
    APPROVED = "approved", "Approved"


class News(TimestampAbstractModel, models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field("Content", config_name="extends")
    category = TreeForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_category",
    )
    slug = models.SlugField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=NewsStatus.choices,
        default=NewsStatus.DRAFT,
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, related_name="created_by"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self._state.adding and self.status == NewsStatus.DRAFT:
            self.status = NewsStatus.PENDING_REVIEW

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Comment(TimestampAbstractModel, MPTTModel):
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self):
        return self.body[:10]
