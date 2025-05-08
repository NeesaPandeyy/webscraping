import os

import requests
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from dotenv import load_dotenv
from mptt.admin import MPTTModelAdmin

from .models import (Announcement, Category, Keyword, News, NewsStatus, Sector,
                     StockNewsURL, StockNewsURLRule, StockRecord, Symbol)

load_dotenv()

admin.site.site_header = "Web Scraping"


class StockKeywordAutoCompleteFilter(AutocompleteFilter):
    title = "Symbol"
    field_name = "symbol"


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)

    def __str__(self):
        return self.name


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)

    def __str__(self):
        return self.name


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ("name",)

    change_list_template = "scraper/symbol_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "symbol_list/",
                self.admin_site.admin_view(self.fetch_symbols_view),
                name="fetch_symbols",
            ),
        ]
        return custom_urls + urls

    def fetch_symbols_view(self, request):
        self.fetch_from_api()
        self.message_user(request, "Data fetched successfully.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def fetch_from_api(self):
        url = os.getenv("STOCK_API_URL")
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                symbols = data.get("results", [])
                for item in symbols:
                    sector_data = item.get("sector")
                    sector_instance = None
                    if sector_data:
                        sector_instance, _ = Sector.objects.get_or_create(
                            sector=sector_data["symbol"],
                            defaults={"name": sector_data["name"]},
                        )

                    Symbol.objects.update_or_create(
                        name=item["symbol"],
                        defaults={"full_name": item["name"], "sector": sector_instance},
                    )

                url = data.get("pagination", {}).get("next")
            else:
                break

    def fetch_from_api_action(self, request, queryset):
        self.fetch_from_api()
        self.message_user(request, "Data fetched successfully.")


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("get_symbols", "title", "url", "summary", "date")
    list_filter = ("symbol", "date", "keywords")
    autocomplete_fields = ("symbol",)
    search_fields = ("title", "keywords__name")

    def get_symbols(self, obj):
        return obj.symbol.name

    get_symbols.short_description = "Symbols"


@admin.register(StockNewsURLRule)
class StockNewsURLRuleAdmin(admin.ModelAdmin):
    list_display = ["url"]
    search_fields = ("url",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "slug", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "description")
    actions = ["approve_news"]

    def approve_news(self, request, queryset):
        updated = queryset.update(status=NewsStatus.PUBLISHED)
        self.message_user(request, "Your post has been approved and published")

    approve_news.short_description = "Mark selected news as Published"

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["status"]
        return super().get_readonly_fields(request, obj)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)
    mptt_level_indent = 20


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("date", "url", "announcement")
    search_fields = ("announcement",)
    list_filter = ("date",)
    ordering = ("-date",)


admin.site.register(StockNewsURL)
