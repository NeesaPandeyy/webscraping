from django.db import models


class Symbol(models.Model):
    name = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.full_name})"


class Keyword(models.Model):
    keyword = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.keyword


class NewsURL(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url


class NewsURLRule(models.Model):
    url = models.ForeignKey(
        NewsURL, on_delete=models.CASCADE, related_name="news_rules"
    )
    search = models.CharField(max_length=100, null=True, blank=True)
    search_bar = models.CharField(max_length=100, null=True, blank=True)
    main_div = models.CharField(max_length=100, null=True, blank=True)
    div_list = models.CharField(max_length=100, null=True, blank=True)
    headline = models.CharField(max_length=50, null=True, blank=True)
    summary_class = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.url)


class SymbolKeywordRelation(models.Model):
    symbol = models.ForeignKey(
        Symbol, on_delete=models.CASCADE, related_name="stock_symbols"
    )
    keywords = models.ManyToManyField(Keyword, related_name="news_keywords", blank=True)

    def __str__(self):
        return f"{self.symbol} - {', '.join([keyword.keyword for keyword in self.keywords.all()])}"


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
    symbol = models.ManyToManyField(Symbol, related_name="symbol")
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return ", ".join(self.symbol.values_list("name", flat=True))
