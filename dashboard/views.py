from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View
from .models import StockRecord


class HomeView(View):
    def get(self, request):
        data = StockRecord.objects.all()
        return render(request, "dashboard/home.html", {"data": data})


class AddDataView(View):
    def get(self, request):
        pass
        # form = ScrapedDataForm()
        # return render(request, "dashboard/add_data.html", {"form": form})

    def post(self, request):
        pass
        # form = ScrapedDataForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, "Data Added")
        #     return redirect("home")
        # return render(request, "dashboard/add_data.html", {"form": form})


class EditDataView(View):
    def get(self, request, sn):
        pass
        # record = get_object_or_404(News, sn=sn)
        # form = ScrapedDataForm(instance=record)
        # return render(request, "dashboard/edit_data.html", {"form": form})

    def post(self, request, sn):
        pass
        # record = get_object_or_404(News, sn=sn)
        # form = ScrapedDataForm(request.POST, instance=record)
        # if form.is_valid():
        #     form.save()
        #     return redirect("home")
        # return render(request, "dashboard/edit_data.html", {"form": form})


class DeleteDataView(View):
    def post(self, request, sn):
        pass
        # record = get_object_or_404(News, sn=sn)
        # record.delete()
        # return redirect("home")


class GenerateActionView(View):
    def get(self, request, sn):
        pass
        # if News:
        #     all_news = get_object_or_404(News, sn=sn)
        #     news_urls = NewsURL.objects.values_list("url", flat=True)
        #     key_word = all_news.key_word
        #     matched_news = all_news(all_news, news_urls, key_word)
        #     title_summary = get_details()
        #     return render(
        #         request,
        #         "dashboard/generate.html",
        #         {"matched_news": matched_news, "title_summary": title_summary},
        #     )

        # elif StockNews:
        #     stocknews = get_object_or_404(StockNews, sn=sn)
        #     key_word = stocknews.symbol
        #     stock_news_urls = StockNewsURL.objects.values_list("url", flat=True)
        #     matched_news = stocknews(stocknews, stock_news_urls, key_word)
        #     title_summary = get_details()
        #     return render(
        #         request,
        #         "dashboard/generate.html",
        #         {"matched_news": matched_news, "title_summary": title_summary},
        #     )

    def post(self, request, sn):
        pass
        # if News:
        #     all_news = get_object_or_404(News, sn=sn)
        #     news_urls = NewsURL.objects.values_list("url", flat=True)
        #     key_word = all_news.key_word
        #     matched_news = all_news(all_news, news_urls, key_word)
        #     return render(
        #         request, "dashboard/generate.html", {"matched_news": matched_news}
        #     )

        # elif StockNews:
        #     stocknews = get_object_or_404(StockNews, sn=sn)
        #     stock_news_urls = StockNewsURL.objects.values_list("url", flat=True)
        #     key_word = stocknews.key_word
        #     matched_news = scrape_stock_news(stocknews, stock_news_urls, key_word)
        #     return render(
        #         request, "dashboard/generate.html", {"matched_news": matched_news}
        #     )


class DownloadView(View):
    def get(self, request):
        pass


class OutputView(View):
    pass
    # def get(self, request):
    #     matched_news = calculate_sentiment()
    #     return render(request, "dashboard/output.html", {"matched_news": matched_news})
