from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.generic import View
from .storage import s3_client, FileUpload  # S3 storage와 통신하기 위한 모듈
from .models import FileInfo  # FileInfo 스키마 가져옴
from .serializers import FileInfoSerializer, UploadSerializer  # fileinfo 모델에 대한 정보를 가져오는 serializer 정의 후 import
from rest_framework import viewsets, status
from rest_framework.views import APIView  # 클래스로 정의되는 APIView 사용

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = UploadSerializer

    def list(self, request):
        if request.user.is_authenticated:
            fileList = FileInfo.objects.filter(owner=request.user)
            response_data = {}
            response_data["file_list"] = []
            for f in fileList:
                serializer = FileInfoSerializer(f)
                response_data["file_list"].append(serializer.data)

            return Response(response_data)
        else:
            return Response("로그인된 상태가 아닙니다.")

    def create(self, request):
        if not request.user.is_authenticated:  # 업로드 시 auth가 없다면 login으로 돌아감
            return Response("로그인된 상태가 아닙니다.")

        response_data = {}
        response_data["uploaded_file_list"] = []

        # serializer 활용 upload
        for f in request.FILES.getlist("files"):
            file_key, file_url = FileUpload(s3_client).upload(f)
            info = FileInfo(title=f.name, url=file_url, owner=request.user, key=file_key)
            info.save()
            serializer = FileInfoSerializer(info,data= request.data)
            if serializer.is_valid():
                serializer.save()
                response_data["uploaded_file_list"].append(serializer.data)

        return Response(response_data)

    def retrieve(self, request, pk=None):
        f = get_object_or_404(self.queryset, pk=pk)
        serializer = FileInfoSerializer(f)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def getShareURL(self, request, pk=None, duration = 3600):
        f = get_object_or_404(self.queryset, pk=pk)
        url, datetime = s3_client.getPresignedURL(f.key, duration)
        response_data = {}
        response_data["url"] = url
        response_data["expireDatetime"] = datetime

        return Response(response_data)

