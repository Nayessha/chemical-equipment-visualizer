from django.urls import path
from .views import UploadCSVView, history_view

urlpatterns = [
    path("upload/", UploadCSVView.as_view()),
    path("history/", history_view),
]
