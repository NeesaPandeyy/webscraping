from django.views.generic import TemplateView
from elasticsearch_dsl.query import Q
from search.documents import NewsPostIndex, StockRecordIndex


class SearchAllView(TemplateView):
    template_name = "search.html"

    def get_query(self):
        return self.request.GET.get("q", "")

    def get_news_search_results(self, query):
        q_news = Q(
            "multi_match",
            query=query,
            fields=["title", "description", "tags"],
            fuzziness="auto",
        )
        search = NewsPostIndex.search().query(q_news)[:50]
        return list(search), search.count()

    def get_stock_search_results(self, query):
        q_stock = Q(
            "multi_match",
            query=query,
            fields=["title", "summary", "symbol"],
            fuzziness="auto",
        )
        search = StockRecordIndex.search().query(q_stock)[:50]
        return list(search), search.count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.get_query()

        news_results, news_total = [], 0
        stock_results, stock_total = [], 0

        if query:
            news_results, news_total = self.get_news_search_results(query)
            stock_results, stock_total = self.get_stock_search_results(query)

        context.update(
            {
                "query": query,
                "news_results": news_results,
                "stock_results": stock_results,
                "news_total": news_total,
                "stock_total": stock_total,
            }
        )
        return context
