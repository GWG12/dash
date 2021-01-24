#import magic
import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Extensión de archivo no válida.')


'''def validate_mime_type(value):
    supported_types=['application/pdf',]
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        mime_type=m.id_buffer(value.file.read(1024))
        value.file.seek(0)
    if mime_type not in supported_types:
        raise ValidationError(u'Tipo de archivo no válido.')

def validate_file_extension_test(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError(u'Error message')
'''

'''
def file_path_mime(file_path):
    supported_types=['application/pdf',]
    mime = magic.from_file(file_path, mime=True)
    if mime not in supported_types:
        raise ValidationError(u'Tipo de archivo no válido.')
    else:
        return mime
'''
