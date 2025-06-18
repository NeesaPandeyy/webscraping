from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

from core.models import TimestampAbstractModel

from .managers import BookmarkManager, LikeManager


class CustomTag(TagBase):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class TaggedNewsPost(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        related_name="tag_items",
        on_delete=models.CASCADE,
    )


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


class NewsPost(TimestampAbstractModel, models.Model):
    class NewsStatus(models.TextChoices):
        PUBLISHED = "published", "Published"
        DRAFT = "draft", "Draft"
        PENDING_REVIEW = "pending_review", "Pending Review"
        REJECTED = "rejected", "Rejected"
        APPROVED = "approved", "Approved"

    title = models.CharField(max_length=500)
    description = RichTextUploadingField(
        config_name="default",
    )
    category = TreeForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_category",
    )
    tags = TaggableManager(through="TaggedNewsPost", blank=True)
    slug = models.SlugField(allow_unicode=True, blank=True, max_length=500)
    status = models.CharField(
        max_length=20,
        choices=NewsStatus.choices,
        default=NewsStatus.DRAFT,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name="created_by",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        if self._state.adding and self.status == self.NewsStatus.DRAFT:
            self.status = self.NewsStatus.PENDING_REVIEW

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.like_set.count()

    class Meta:
        verbose_name = "Post News"
        verbose_name_plural = "Post News"


class Like(TimestampAbstractModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

    objects = LikeManager()

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} liked {self.post}"


class Comment(TimestampAbstractModel, MPTTModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        NewsPost, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self):
        return self.body[:10]


class Bookmark(TimestampAbstractModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

    objects = BookmarkManager()

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} bookmarked {self.post}"
