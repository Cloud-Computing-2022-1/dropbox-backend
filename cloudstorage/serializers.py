from .models import FileInfo
from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField


# fileinfo 모델의 속성들 중 views.py에서 사용된 FileUploadView의 info를 json 형태로 변환하기 위한 serializer


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ["title", "url", "owner", "key"]

class UploadSerializer(Serializer):
    files = FileField()
    class Meta:
        fields = ['files']