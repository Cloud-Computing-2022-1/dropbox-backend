from django.db import models
from django.contrib.auth.models import User


# 파일 세부 정보 관련 모델
# title, url, owner, key는 null=true이므로 file 생성 시 파라미터 없이 생성을 허용
# self 함수 호출시 title 반환
class FileInfo(models.Model):
    file_path = models.TextField(max_length=100,default="/")
    title = models.TextField(max_length=40, null=True)
    url = models.URLField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    key = models.TextField(max_length=40, null=True)
    script = models.TextField(null=True, blank=True, verbose_name="동영상 스크립트")

    def __str__(self):
        return self.title

def get_default_tree():
        return {'root': {}}

class FolderTree(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tree = models.JSONField(default=get_default_tree)

    