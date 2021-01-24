from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import FilesUpload, FilesUploadPrivate
from .forms import FilesUploadForm

def image_upload(request):
    form = FilesUploadForm(request.POST)

    if request.method == 'POST':
        print(request.FILES)
        #print(wegiwoiegb)
        form = FilesUploadForm(request.POST, request.FILES)
        print("ERRORES FORMA ",form.errors)
        if form.is_valid():
            print(form)
            form.save()
            return render(request, 'amazon/bucket.html', {
                'image_url': image_url
            })
    return render(request, 'amazon/bucket.html',{'form':form})
