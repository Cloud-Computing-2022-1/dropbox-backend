from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.generic import View
from .storage import s3_client, FileUpload  # S3 storage와 통신하기 위한 모듈
from .models import FileInfo, FolderTree  # FileInfo 스키마 가져옴
from .serializers import CreateFolderSerializer, DeleteFolderSerializer, FileInfoSerializer, FolderTreeSerializer, SearchSerializer, UploadSerializer  # fileinfo 모델에 대한 정보를 가져오는 serializer 정의 후 import
from rest_framework import viewsets, status
from rest_framework.views import APIView  # 클래스로 정의되는 APIView 사용

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import re

@method_decorator(csrf_exempt, name='dispatch')
class FileViewSet(viewsets.ModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = UploadSerializer

    def list(self, request):
        self.serializer_class = UploadSerializer
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
        self.serializer_class = UploadSerializer
        if not request.user.is_authenticated:  # 업로드 시 auth가 없다면 login으로 돌아감
            return Response("로그인된 상태가 아닙니다.")

        response_data = {}
        response_data["uploaded_file_list"] = []

        exp = re.compile("^([\/]{1}[a-z0-9]+)+(\/){1}$|^([\/]{1})$")
        filePath = request.data.get('file_path')
        if not exp.match(filePath):
            return Response("잘못된 path 형식입니다.")

        tree = FolderTree.objects.get(owner=request.user)
        serializer = FolderTreeSerializer(tree)
        treeDict = serializer.data
        
        rootDict = treeDict['tree']['root']
        pathList = request.data.get("file_path").split('/')
        if len(pathList) <= 2:
            pass
        else:
            result = searchDict(rootDict, pathList[-2])
            if filePath not in result:
                return Response("존재하지 않는 path 입니다.")

        

        # serializer 활용 upload
        for f in request.FILES.getlist("files"):
            file_key, file_url = FileUpload(s3_client).upload(f)
            info = FileInfo(title=f.name, url=file_url, owner=request.user, key=file_key, file_path=request.data.get('file_path'))
            info.save()
            serializer = FileInfoSerializer(info,data= request.data)
            if serializer.is_valid():
                serializer.save()
                response_data["uploaded_file_list"].append(serializer.data)

        return Response(response_data)

    def retrieve(self, request, pk=None):
        self.serializer_class = FileInfoSerializer
        f = FileInfo.objects.get(id=pk)
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



@method_decorator(csrf_exempt, name='dispatch')
class FolderTreeViewSet(viewsets.ModelViewSet):
    queryset = FolderTree.objects.all()
    serializer_class = CreateFolderSerializer

    def list(self, request):
        if request.user.is_authenticated:
            tree = FolderTree.objects.get(owner=request.user)
            serializer = FolderTreeSerializer(tree)

            return Response(serializer.data)
        else:
            return Response("로그인된 상태가 아닙니다.")

    def create(self, request):
        if not request.user.is_authenticated:
            return Response("로그인된 상태가 아닙니다.")

        tree = FolderTree.objects.get(owner=request.user)
        serializer = FolderTreeSerializer(tree)
        treeDict = serializer.data
        pathList = request.data.get("file_path").split('/')
        
        cur = treeDict['tree']['root']
        
        for path in pathList:
            if path == '':
                continue
            cur = cur[path]
        cur[request.data.get("name")] = {}
        tree.tree = treeDict['tree']
        tree.save()

        serializer = FolderTreeSerializer(tree)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFolderViewSet(viewsets.GenericViewSet):
    serializer_class = DeleteFolderSerializer

    def list(self, request):
        if request.user.is_authenticated:
            tree = FolderTree.objects.get(owner=request.user)
            serializer = FolderTreeSerializer(tree)

            return Response(serializer.data)
        else:
            return Response("로그인된 상태가 아닙니다.")

    def create(self, request):
        if not request.user.is_authenticated:
            return Response("로그인된 상태가 아닙니다.")

        tree = FolderTree.objects.get(owner=request.user)
        serializer = FolderTreeSerializer(tree)
        treeDict = serializer.data
        pathList = request.data.get("file_path").split('/')
        
        cur = treeDict['tree']['root']
        before = cur
        folderName = ''
        
        for path in pathList:
            if path == '':
                continue
            folderName = path
            before = cur
            cur = cur[path]
        del before[folderName]
        tree.tree = treeDict['tree']
        tree.save()

        serializer = FolderTreeSerializer(tree)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class SearchViewSet(viewsets.GenericViewSet):
    serializer_class = SearchSerializer

    def create(self, request):
        if not request.user.is_authenticated:
            return Response("로그인된 상태가 아닙니다.")

        fileList = FileInfo.objects.filter(owner=request.user)
        fileName = request.data.get("name")
        filePath = request.data.get("file_path")
        if (fileName == ""): #폴더만 검색
            fileList = fileList.filter(file_path__iexact=filePath)
        else:
            fileList = fileList.filter(file_path__iexact=filePath)
            fileList = fileList.filter(title__icontains=fileName) 

        response_data = {}
        response_data["result"] = []
        for f in fileList:
            serializer = FileInfoSerializer(f)
            response_data["result"].append(serializer.data)

        return Response(response_data)

    def searchFolder(self,request,keyword=None):
        if not request.user.is_authenticated:
            return Response("로그인된 상태가 아닙니다.")

        tree = FolderTree.objects.get(owner=request.user)
        serializer = FolderTreeSerializer(tree)
        treeDict = serializer.data
        
        rootDict = treeDict['tree']['root']
        result = searchDict(rootDict, keyword)
        response_data = {}
        response_data["result"] = result

        return Response(response_data)
        


def searchDict(dic, keyword):
    result = []
    keyword = keyword.lower()
    path = "/"
    def search(curDic, curPath):
        for k, v in curDic.items():
            if keyword in k.lower():
                result.append(curPath+f"{k}/")
            search(v, curPath+f"{k}/")

    search(dic,path)
    return result