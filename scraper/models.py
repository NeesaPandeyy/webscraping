from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey

from core.models import TimestampAbstractModel


class Sector(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=225, unique=True)
    sector = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.sector


class Symbol(models.Model):
    name = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name="sectortype", null=True
    )

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StockNewsURL(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url


class StockNewsURLRule(models.Model):
    url = models.ForeignKey(
        StockNewsURL, on_delete=models.CASCADE, related_name="rules"
    )
    click_button = models.CharField(max_length=150, null=True, blank=True)
    main_div = models.CharField(max_length=50, null=True, blank=True)
    div_list = models.CharField(max_length=100, null=True, blank=True)
    tbody = models.CharField(max_length=50, null=True, blank=True)
    rows = models.CharField(max_length=50, null=True, blank=True)
    uploaded = models.CharField(max_length=50, null=True, blank=True)
    headline = models.CharField(max_length=50, null=True, blank=True)
    summary_id = models.CharField(max_length=50, null=True, blank=True)
    summary_class = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.url)


class StockRecord(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="symbol")
    keywords = models.ManyToManyField(Keyword, related_name="keywords", blank=True)
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.symbol)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["name"]


class NewsStatus(models.TextChoices):
    PUBLISHED = "published", "Published"
    DRAFT = "draft", "Draft"
    PENDING_REVIEW = "pending_review", "Pending Review"


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    date = models.DateField(null=True, blank=True)
    url = models.URLField(max_length=500)
    announcement = models.TextField(blank=True, null=True)
