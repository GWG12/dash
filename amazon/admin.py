from django.contrib import admin
from .models import FilesUpload, FilesUploadPrivate


admin.site.register(FilesUpload)
admin.site.register(FilesUploadPrivate)
