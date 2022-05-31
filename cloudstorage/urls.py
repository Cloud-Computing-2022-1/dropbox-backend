from django.urls import path
from .views import *

urlpatterns = [
    path('upload', FileUploadView.as_view(), name='uploadfile'),
    path('download', FileDownloadView.as_view(), name='downloadfile'),
]