from django.shortcuts import render, redirect
from django.views.generic import View
from .storage import s3_client, FileUpload
from .models import FileInfo
from urllib.request import urlopen, urlretrieve

class FileUploadView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        for f in request.FILES.getlist('file'):
            file_key, file_url = FileUpload(s3_client).upload(f)
            info = FileInfo(
                title = f.name,
                url = file_url,
                owner = request.user,
                key = file_key
            )
            info.save()
        return redirect('uploadfile')
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'fileupload.html')
        else:
            return redirect('login')


class FileDownloadView(View):
    def get(self, request):
        if request.user.is_authenticated:
            fileList = FileInfo.objects.filter(owner = request.user)

            return render(request, 'filedownload.html', {'fileList':fileList})
        else:
            return redirect('login')