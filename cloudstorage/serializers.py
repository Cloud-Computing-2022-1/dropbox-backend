from email.policy import default
from .models import FileInfo, FolderTree
from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField


# fileinfo 모델의 속성들 중 views.py에서 사용된 FileUploadView의 info를 json 형태로 변환하기 위한 serializer


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ["id","title", "url", "owner", "key", "upload_date","file_path"]

class UploadSerializer(Serializer):
    files = FileField()
    file_path = serializers.CharField(default='/', max_length=100)
    class Meta:
        fields = ['files','file_path']

class FolderTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderTree
        fields = ["id","owner", "tree"]

class CreateFolderSerializer(Serializer):
    file_path = serializers.CharField(default='/', max_length=100)
    name = serializers.CharField(required=True)
    class Meta:
        fields = ['file_path','name']