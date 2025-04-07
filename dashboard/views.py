from django.shortcuts import render
from django.views import View
from .models import StockRecord


class HomeView(View):
    def get(self, request):
        data = StockRecord.objects.all()
        return render(request, "dashboard/home.html", {"data": data})
