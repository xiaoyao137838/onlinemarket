from django.core.exceptions import ValidationError
import os

def validate_picture_format(data):
    pic_format = os.path.splitext(data.name)[1]
    valid_formats = ['.png', '.jpg', '.jpeg']
    if pic_format.lower() in valid_formats:
        return True
    else:
        raise ValidationError('Unsupported file format. Allowed formats: ' + str(valid_formats))