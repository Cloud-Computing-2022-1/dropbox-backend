from django.urls import path, include
from .views import FileViewSet, FolderTreeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'folders', FolderTreeViewSet)

fileList = FileViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
    }
)

fileDetail = FileViewSet.as_view(
    {
        'get': 'retrieve',
        # 'put': 'update',
        # 'patch': 'partial_update',
        'delete': 'destroy',
    }
)

fileShare = FileViewSet.as_view(
    {
        'get': 'getShareURL'
    }
)

urlpatterns = [
    path('', fileList),
    path('<int:pk>/', fileDetail),
    path('<int:pk>/share/<int:duration>', fileShare),
]
