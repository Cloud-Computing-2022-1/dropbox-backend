from collections import UserDict
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# User 정보 중 userId 를 json으로 변환하기 위한 serializer
# views.py에 django의 기본 user 생성 기능을 이용하였으므로 import하여 해당 모델을 그대로 사용


class UserSerializer(serializers.ModelSerializer):
    #confirm = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        # User를 모델로 하는 serializer에 대해서, validate function을 override함(password와 confirm의 일치 여부를 가지고 판별)
        # password는 비밀번호이며, confirm은 비밀번호를 확인하기 위해 다시 한번 적는 부분이다
        def validate(self, data):
            # if data["password"] != data["confirm"]:
            #     raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다")
            return data

        # user object create하는 단계
        # confirm이라는 확인만을 위한 정보를 제외하고 새로운 user object 생성
        def create(self, validated_data):
            # validated_data.pop("confirm")
            user = User.objects.create(**validated_data)
            user.set_password(validated_data["password"])
            user.save()

            return user

        # user 정보 업데이트
        def update(self, instance, validated_data):
            instance.username = validated_data["username"]
            instance.password = validated_data["password"]
            instance.email = validated_data["email"]
            instance.save()

            return instance


# 로그인 기능을 위한 serializer / authenticate는 data에서 username과 password를 받아서 유저가 존재하면 user 객체를, 존재하지 않을 시 none을 리턴
class loginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def perform_login(self, request):  # login 기능 수행(request에 따른 username과 password를 가지고 수행)
            user = authenticate(username=request.data["username"], password=request.data["password"])
            login(request, user)
            return user

    def validate(self, data):  # 들어온 데이터에 대해 유저가 존재하는지 여부를 확인
            user = authenticate(username=data["username"], password=data["password"])
            if user is None:
                raise serializers.ValidationError("아이디 혹은 비밀번호가 잘못되었습니다")
            return data

    class Meta:
        fields = ["username","password"]

class logoutSerializer(serializers.Serializer):
    pass