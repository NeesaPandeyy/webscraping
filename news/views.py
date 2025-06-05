from django.shortcuts import redirect, render

from .forms import NewsPostAdminForm
from .models import NewsPost


def create_news_view(request):
    if request.method == "POST":
        form = NewsPostAdminForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.creator = request.user
            news.save()
            form.save_m2m()
            return redirect("news-list")
    else:
        form = NewsPostAdminForm()
    return render(request, "news/createnews.html", {"form": form})


def published_news_view(request):
    news_list = NewsPost.objects.filter(status="published").order_by("-created_at")
    return render(request, "news/publishednews.html", {"news_list": news_list})
