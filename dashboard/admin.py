from django.contrib import admin
import requests
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import (
    StockRecord,
    StockNewsURLRule,
    NewsURLRule,
    NewsURL,
    StockNewsURL,
    Symbol,
    SymbolKeywordRelation,
    Keyword,
    SymbolKeywordRelation
    
)
from scraper.services import stock_news,keyword_data
from admin_auto_filters.filters import AutocompleteFilter
from django.shortcuts import get_object_or_404

admin.site.site_header = "Web Scraping"


class StockKeywordAutoCompleteFilter(AutocompleteFilter):
    title = "Symbol"
    field_name = "symbol"

class KeywordAutoCompleteFilter(AutocompleteFilter):
    title = "Keyword"
    field_name = "keywords"


@admin.register(Keyword)
class KeywordsAdmin(admin.ModelAdmin):
    list_display = ["keyword"]
    search_fields = ("keyword",)


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)

    change_list_template = "admin/symbol_list.html" 

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('symbol_list/', self.admin_site.admin_view(self.fetch_symbols_view), name='fetch_symbols'),
        ]
        return custom_urls + urls
    
    def fetch_symbols_view(self, request):
        self.fetch_from_api() 
        self.message_user(request, "Data fetched successfully.")  
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
    def fetch_from_api(self):
        url = "https://dev.nepsetrends.com/api/stock/"
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                symbols = data.get("results",[])
                for symbol in symbols:
                    Symbol.objects.update_or_create(
                        name=symbol["symbol"],
                        defaults={"full_name": symbol["name"]}
                    )
                pagination = data.get("pagination",{})
                url=pagination.get("next")
        
    def fetch_from_api_action(self,request,querset):
        self.fetch_from_api()
        self.message_user(request, "data fetched successfully.")
     

@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ("get_symbols", "title", "url")
    list_filter = ( "symbol",)
    autocomplete_fields = ("symbol",)
    search_fields = ("title",)

    
    def get_symbols(self, obj):
        return ", ".join(obj.symbol.values_list("name", flat=True))
    
    # change_form_template = "dashboard/button.html"

    # def response_change(self, request, obj):
    #     if "_generate" in request.POST:
    #         matched_news = keyword_data()
    #         return render(
    #             request, "dashboard/generate.html", {"matched_news": matched_news}
    #         )
    #     if "_details" in request.POST:
    #         get_details()
    #         return HttpResponseRedirect(request.path)

    #     if "_sentiment" in request.POST:
    #         sentiment = calculate_sentiment()
    #         return render(request, "dashboard/output.html", {"sentiment": sentiment})

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk: 
    #         obj.created_by = request.user
    #     obj.updated_by = request.user
    #     obj.save()
    
    get_symbols.short_description = "Symbols"

@admin.register(NewsURLRule)
class NewsURLRuleAdmin(admin.ModelAdmin):
    list_display = ["url"]
    search_fields = ("url",)

@admin.register(StockNewsURLRule)
class StockNewsURLRuleAdmin(admin.ModelAdmin):
    list_display = ["url"]
    search_fields = ("url",)

admin.site.register(NewsURL)
admin.site.register(StockNewsURL)
# admin.site.register(NewsURLRule)
# admin.site.register(StockNewsURLRule)

@admin.register(SymbolKeywordRelation)
class SymbolKeywordRelationAdmin(admin.ModelAdmin):
    list_display = ("get_keywords", "symbol") 
    list_filter = (KeywordAutoCompleteFilter, StockKeywordAutoCompleteFilter)  
    search_fields = ("keywords__keyword", "symbol") 
    autocomplete_fields = ("symbol","keywords")

    def get_keywords(self, obj):
        return ", ".join([keyword.keyword for keyword in obj.keywords.all()])
    get_keywords.short_description = "Keywords"

    change_form_template = "dashboard/button.html"

    def response_change(self, request, obj):
        if "_generate" in request.POST:
            pk = obj.pk
            records = get_object_or_404(SymbolKeywordRelation,pk=pk)
            keywords = [kw.keyword for kw in records.keywords.all()]
            symbol = records.symbol
            matched_news = keyword_data(symbol,keywords)
            return render(
                request, "dashboard/generate.html", {"matched_news": matched_news}
            )