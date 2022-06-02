from distutils.filelist import FileList
from django.urls import path, include
from .views import FileUploadViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'upload', FileUploadViewSet)
# UserViewSet은 UserSerializer를 통해 생성되는데, UserSerializer는 내부에 validity check, create 함수를 보유하고

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # 별도 signup을 위한 api를 가지지 않고도, accounts/ url을 사용하면 router를 통해서 유저를 생성할 수 있음
]
