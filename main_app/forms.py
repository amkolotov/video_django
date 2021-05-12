import os

from mutagen.mp4 import MP4

from django import forms
from django.core.exceptions import ValidationError

from .models import Video


class VideoCreateForm(forms.ModelForm):
    """Форма для добавления видео"""
    class Meta:
        model = Video
        fields = ('title', 'description', 'video')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_video(self):
        file = self.cleaned_data.get('video', False)
        if file:
            if file.content_type not in ['video/mp4']:
                raise ValidationError("Файл должен быть типа MP4")
            if not os.path.splitext(file.name)[1] in ['.mp4']:
                raise ValidationError("У файла должно быть расширение mp4")
            if file.size > 200 * 1024 * 1024:
                raise ValidationError("Видео файл слишком большой ( > 200mb )")
            if int(MP4(file).info.length) > 180:
                raise ValidationError("Продолжительность видео не должна превышать 3 минуты")
            return file
        else:
            raise ValidationError("Невозможно прочитать загружаемый файл")
