from django.db import models
from dashboard.storage_backends import PublicMediaStorage, PrivateMediaStorage
from .validators import validate_file_extension


#Creates custom path where files will be saved
def custom_path(instance, filename):
    # file will be uploaded to AMAZON_ROUTE/project_name/filename
    return f'{instance.project_name}/{filename}'

class FilesUpload(models.Model):
    project_name = models.CharField(max_length=150)
    #image = models.FileField(storage=PublicMediaStorage(),upload_to=custom_path,
    #validators=[validate_file_extension])
    image = models.FileField(storage=PublicMediaStorage(),upload_to=custom_path)
    #text = models.FileField(storage=PublicMediaStorage())

    def __str__(self):
        return f'{self.project_name} Proyecto'

class FilesUploadPrivate(models.Model):
    project_name = models.CharField(max_length=150)
    image = models.FileField(storage=PrivateMediaStorage())
    #text = models.FileField(storage=PrivateMediaStorage())

    def __str__(self):
        return f'{self.project_name} Proyecto'
