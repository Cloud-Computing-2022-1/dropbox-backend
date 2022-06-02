from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.generic import View
from .storage import s3_client, FileUpload  # S3 storage와 통신하기 위한 모듈
from .models import FileInfo  # FileInfo 스키마 가져옴
from .serializers import FileInfoSerializer, UploadSerializer  # fileinfo 모델에 대한 정보를 가져오는 serializer 정의 후 import
from rest_framework import viewsets
from rest_framework.views import APIView  # 클래스로 정의되는 APIView 사용

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if not request.user.is_authenticated:  # 업로드 시 auth가 없다면 login으로 돌아감
            return redirect("login")

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


# 파일 다운로드 과정에서 response에 serializer를 적용하여 json 형식으로 받아옴 response로 받아올 정보들을 list에 담아서 렌더링
@method_decorator(csrf_exempt, name='dispatch')
class FileDownloadView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            fileList = FileInfo.objects.filter(owner=request.user)
            response_data = {}
            response_data["file_list"] = []
            for f in fileList:
                serializer = FileInfoSerializer(f)
                response_data["file_list"].append(serializer.data)

            return Response(response_data)
        else:
            return redirect("login")


"""
class FileUploadView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:  # 업로드 시 auth가 없다면 login으로 돌아감
            return redirect("login")


        for f in request.FILES.getlist("file"):  # auth가 있는 경우
            file_key, file_url = FileUpload(s3_client).upload(f)
            info = FileInfo(title=f.name, url=file_url, owner=request.user, key=file_key)
            info.save()
        return redirect("uploadfile")

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "fileupload.html")
        else:
            return redirect("login")


class FileDownloadView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            fileList = FileInfo.objects.filter(owner=request.user)

            return render(request, "filedownload.html", {"fileList": fileList})
        else:
            return redirect("login")
"""

# serializer를 이용하여 DB의 모든 FileInfo 인스턴스를 json 타입으로 변환
# 보통 다수의 정보를 받아올 때 serializer를 활용하여 json 타입으로 저장


class FileListAPI(APIView):
    def get(self, request):
        queryset = FileInfo.objects.all()
        serializer = FileInfoSerializer(queryset, many=True)
        return Response(serializer.data)
