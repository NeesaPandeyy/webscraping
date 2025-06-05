from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from news.models import NewsPost
from scraper.models import StockRecord

news_post_index = Index("news_posts")
stock_record_index = Index("stock_records")


@registry.register_document
class NewsPostIndex(Document):
    title = fields.TextField()
    description = fields.TextField()
    category = fields.KeywordField()
    tags = fields.KeywordField(multi=True)

    class Index:
        name = "news_posts"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = NewsPost
        fields = ["id"]

    def prepare_category(self, instance):
        return str(instance.category) if instance.category else ""

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]


@registry.register_document
class StockRecordIndex(Document):
    symbol = fields.KeywordField()
    keywords = fields.KeywordField(multi=True)
    title = fields.TextField()
    summary = fields.TextField()

    class Index:
        name = "stock_records"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = StockRecord
        fields = ["id"]

    def prepare_symbol(self, instance):
        return str(instance.symbol)

    def prepare_keywords(self, instance):
        return [kw.word for kw in instance.keywords.all()]
