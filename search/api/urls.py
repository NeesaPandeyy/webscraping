from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsPostViewset, SearchAPIRootView, StockRecordViewset

router = DefaultRouter()
router.register(r"stockrecord", StockRecordViewset, basename="stockrecorddocument-api")
router.register(r"newsrecord", NewsPostViewset, basename="newsrecorddocument-api")

urlpatterns = [
    path("", SearchAPIRootView.as_view(), name="api-search"),
    path("documents/", include(router.urls)),
]
