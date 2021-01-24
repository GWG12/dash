from django import forms
from .models import FilesUpload, FilesUploadPrivate
from django.contrib.auth.models import User
import zipfile


class FilesUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesUploadForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        #self.fields['text'].required = True

    class Meta:
        model = FilesUpload
        fields = [
            'project_name',
            'image',
            #'text',
        ]

    def clean_image(self):

        supported_types=['jpg',]
        files = self.cleaned_data['image']
        zip = zipfile.ZipFile(files)
        print(zip.namelist())
        for file in zip.namelist():
            print(file.split('.')[1].lower())
            if not file.split('.')[1].lower() in supported_types:
                raise forms.ValidationError('Solo se permiten archivos pdf')
        return files

    '''
    def clean_image(self):
        supported_types=['application/pdf',]
        file = self.cleaned_data['image']
        try:
            if file:
                file_type = file.content_type.split('/')[0]
                print("TIPO DE ARCHIVO", file_type)

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type in supported_types:
                    if file._size > "5242880":
                        raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
                else:
                    raise forms.ValidationError(_('File type is not supported'))
        except:
            pass

        return file
        '''

class FilesUploadPrivateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesUploadPrivateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        #self.fields['text'].required = True

    class Meta:
        model = FilesUploadPrivate
        fields = [
            'project_name',
            'image',
            #'text',
        ]
