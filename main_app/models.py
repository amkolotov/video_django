import datetime

from django.conf import settings
from django.db import models


def file_name(instance, filename):
    filename = f'{datetime.datetime.utcnow()}.mp4'
    return '/'.join(['videos', instance.author.username, filename])


class Video(models.Model):
    """Модель видео"""
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    preview = models.ImageField('Превью')
    video = models.FileField('Видео', upload_to=file_name)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
