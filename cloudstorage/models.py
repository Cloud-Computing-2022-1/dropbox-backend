from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FileInfo(models.Model):
    title = models.TextField(max_length=40, null=True)
    url = models.URLField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    key = models.TextField(max_length=40, null=True)

    def __str__(self):
        return self.title