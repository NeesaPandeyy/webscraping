from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from news.models import NewsPost
from scraper.models import StockRecord
from search.documents import NewsPostIndex, StockRecordIndex


@receiver(post_save, sender=NewsPost)
def index_newspost(sender, instance, **kwargs):
    NewsPostIndex().update(instance)


@receiver(post_delete, sender=NewsPost)
def delete_newspost(sender, instance, **kwargs):
    NewsPostIndex().delete(instance)


@receiver(post_save, sender=StockRecord)
def index_stockrecord(sender, instance, **kwargs):
    StockRecordIndex().update(instance)


@receiver(post_delete, sender=StockRecord)
def delete_stockrecord(sender, instance, **kwargs):
    StockRecordIndex().delete(instance)
