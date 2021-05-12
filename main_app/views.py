import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import VideoCreateForm
from .models import Video
from .services import get_preview, stream_video


class CreateVideoView(LoginRequiredMixin, CreateView):
    """Добавление нового видео"""
    template_name = 'main_app/add_video.html'
    form_class = VideoCreateForm
    success_url = reverse_lazy('main_app:video_list')

    def post(self, request, *args, **kwargs):
        form = VideoCreateForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.preview = os.path.join('previews', get_preview(form.cleaned_data.get('video').temporary_file_path()))
            video.save()
            return redirect(reverse('main_app:video_list'))
        return render(request, 'main_app/add_video.html', {'form': form})


class VideoListView(ListView):
    """Вывод списка видео"""
    model = Video


class UserVideoListView(LoginRequiredMixin, ListView):
    """Вывод видео пользователя"""

    def get_queryset(self):
        return Video.objects.filter(author=self.request.user)


class VideoView(View):
    """Страница просмотра видео"""
    def get(self, request, video_pk):
        video = get_object_or_404(Video, pk=video_pk)
        return render(request, 'main_app/video.html', {'video': video})


class PlayerStreamView(View):
    """Потоковое транслирование видео"""
    def get(self, request, video_pk):
        video = get_object_or_404(Video, pk=video_pk)
        return stream_video(request, video.video.url)
