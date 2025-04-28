from celery import shared_task

from .services import StockNewscore


@shared_task(name="scheduling")
def stocknews_scraping():
    scrape = StockNewscore()
    return scrape.stock_news()
