"""dropbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import accounts
from rest_framework import routers
from accounts.views import UserViewSet, LoginViewSet, LogoutViewSet
from cloudstorage.views import FileViewSet, FileViewSet, SearchViewSet
from accounts.urls import router as accountsRouter
from cloudstorage.urls import router as cloudstorageRouter

# 보유중인 url
"""
admin/

accounts/home
accounts/home/signup
accounts/home/login
accounts/home/logout

storage/upload
storage/download
storage/list
"""

router = routers.DefaultRouter()
router.registry.extend(accountsRouter.registry)
router.registry.extend(cloudstorageRouter.registry)

searchFolder = SearchViewSet.as_view(
    {
        'get': 'searchFolder',
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path('files/',include('cloudstorage.urls')),
    path('folders/',include('cloudstorage.urls')),
    path('folders/search/<str:keyword>/', searchFolder),
    # path("accounts/", include("accounts.urls")),
    # path("storage/", include("cloudstorage.urls")),
]
