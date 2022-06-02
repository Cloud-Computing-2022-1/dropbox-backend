from django.urls import path, include
from rest_framework import routers
from .views import *
from django.views.decorators.csrf import csrf_exempt

# view에서 APIview를 이용해서 정의한 함수들 import, url에 따른 연산 수행

router = routers.DefaultRouter()
router.register(r"login", LoginViewSet, basename='loginModel')
router.register(r'logout', LogoutViewSet, basename='logoutModel')
router.register(r"user", UserViewSet)

# UserViewSet은 UserSerializer를 통해 생성되는데, UserSerializer는 내부에 validity check, create 함수를 보유하고

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # 별도 signup을 위한 api를 가지지 않고도, accounts/ url을 사용하면 router를 통해서 유저를 생성할 수 있음
]


"""from django.urls import path
from .views import signup, login, logout, home

# view에서 api_view를 이용해서 정의한 함수들 import, url에 따른 연산 수행

urlpatterns = [
    path("home/signup/", signup, name="signup"),
    path("home/login/", login, name="login"),
    path("home/logout/", logout, name="logout"),
    path("home/", home, name="home"),
]
"""
