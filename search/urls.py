from django.urls import path
from search.views import SearchAllView

urlpatterns = [
    path("", SearchAllView.as_view(), name="search_all"),
]
