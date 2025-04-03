from django.urls import path
from .views import (
    HomeView,
    EditDataView,
    GenerateActionView,
    DeleteDataView,
    AddDataView,
    OutputView,
    DownloadView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("add/", AddDataView.as_view(), name="add_data"),
    path("edit/<int:sn>/", EditDataView.as_view(), name="edit_data"),
    path("delete/<int:sn>/", DeleteDataView.as_view(), name="delete_data"),
    path("generate/<int:sn>/", GenerateActionView.as_view(), name="generate_action"),
    path("download/", DownloadView.as_view(), name="download_csv"),
    path("output/", OutputView.as_view(), name="output"),
]
