from django.core.management.base import BaseCommand

from news.models import NewsPost
from scraper.models import StockRecord
from search.documents import NewsPostIndex, StockRecordIndex


class Command(BaseCommand):
    help = "Rebuild Elasticsearch indices for NewsPost and StockRecord models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing indices...")
        NewsPostIndex._index._name = "news_posts"
        NewsPostIndex.init()

        StockRecordIndex._index._name = "stock_records"
        StockRecordIndex.init()

        self.stdout.write("Indexing news posts...")
        NewsPostIndex().update(NewsPost.objects.all())

        self.stdout.write("Indexing stock records...")
        StockRecordIndex().update(StockRecord.objects.all())

        self.stdout.write(self.style.SUCCESS("All data indexed successfully."))
