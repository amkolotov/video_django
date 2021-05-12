import datetime
import mimetypes
import os.path
import re
from typing import Generator
from wsgiref.util import FileWrapper

import cv2
from django.conf import settings
from django.http import StreamingHttpResponse
from mutagen.mp4 import MP4


def get_preview(video) -> str:
    """Получение превью из видео"""
    vidcap = cv2.VideoCapture(video)
    length = int(MP4(video).info.length)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, length // 2 * 1000)
    has_frame, image = vidcap.read()
    filename = f"{datetime.datetime.utcnow()}.jpg"
    filepath = os.path.join(settings.MEDIA_ROOT, 'previews', filename)
    cv2.imwrite(filepath, image)
    return filename


def file_iterator(file_name, chunk_size: int = 8192, start: int = 0, end=None) -> Generator:
    """Создание итератора для потока видео"""
    with open(file_name, "rb") as f:
        f.seek(start, os.SEEK_SET)
        remaining = end
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request, media_path: str) -> StreamingHttpResponse:
    """Создание StreamingHttpResponse"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = f'{settings.BASE_DIR}{media_path}'
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'

    if range_match:
        content_range = range_header.strip().lower().split('=')[-1]
        first_byte, last_byte = map(str.strip, content_range.split('-'))
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(
            file_iterator(path, start=first_byte, end=length),
            status=206,
            content_type=content_type
        )
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'

    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)

    resp['Accept-Ranges'] = 'bytes'
    return resp
