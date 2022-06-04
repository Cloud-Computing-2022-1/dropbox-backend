from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from django.contrib.auth import logout
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, status
from cloudstorage.models import FolderTree

# django.contirb.auth.models의 User를 사용하여 유저를 생성 및 저장

from rest_framework.views import APIView  # 클래스로 정의되는 APIView 사용

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# 모든 사용자 나열/검색 "id", "username", "password", "email" 정보 반환
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )
        user = serializer.Meta.create(serializer.Meta,validated_data=serializer.data)
        folderTree = FolderTree(owner=user)
        folderTree.save()

        response_data = {}
        response_data["Status"] = "Success"
        response_data["Username"] = user.get_username()

        return Response(response_data)

# 로그인 기능 수행을 위한 view. login은 post method로 request를 받음
# import한 loginserializer 활용, loginserializer의 perform_login 함수 수행
@method_decorator(csrf_exempt, name='dispatch')
class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = loginSerializer

    def create(self, request):
        if request.user.is_authenticated:
            return Response("이미 로그인된 상태입니다.")
        serializer = loginSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )  # is_valid가 수행되면 exception이 발생하지 않으며 login 수행, 결과리턴
        user = serializer.perform_login(request)
        response_data = {}
        response_data["Status"] = "Success"
        response_data["Username"] = user.get_username()
        return Response(response_data)


# 로그아웃 기능 수행을 위한 view. request가 들어오면 단순히 로그아웃 시켜줌(함수 수행 x)
@method_decorator(csrf_exempt, name='dispatch')
class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = logoutSerializer
    def create(self, request):
        username = ""
        if request.user.is_authenticated:
            username = request.user.get_username()
            logout(request)
            response_data = {}
            response_data["Status"] = "Success"
            response_data["Username"] = username
            return Response(response_data)
        else:
            return Response("로그인된 상태가 아닙니다.")