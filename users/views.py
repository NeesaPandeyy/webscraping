from django.contrib.auth import logout
from django.shortcuts import redirect, render


def home(request):
    return render(request, "users/home.html")


def logout_view(request):
    logout(request)
    return redirect("/")
