from django.urls import path, include
from rest_framework import routers
from .views import *
from django.views.decorators.csrf import csrf_exempt

# view에서 APIview를 이용해서 정의한 함수들 import, url에 따른 연산 수행

router = routers.DefaultRouter()
router.register(r"login", LoginViewSet, basename='loginModel')
router.register(r'logout', LogoutViewSet, basename='logoutModel')
router.register(r"user", UserViewSet)

userDetail = UserViewSet.as_view(
    {
        #'get': 'retrieve',
        # 'put': 'update',
        # 'patch': 'partial_update',
        'delete': 'destroy',
    }
)

# UserViewSet은 UserSerializer를 통해 생성되는데, UserSerializer는 내부에 validity check, create 함수를 보유하고

urlpatterns = [
    path("", include(router.urls)),
    path('<int:pk>/', userDetail),
]
