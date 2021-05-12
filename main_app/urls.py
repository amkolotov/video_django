from django.urls import path

from .views import CreateVideoView, VideoListView, VideoView, PlayerStreamView, UserVideoListView

app_name = 'main_app'

urlpatterns = [
    path('', VideoListView.as_view(), name='video_list'),
    path('user_video/', UserVideoListView.as_view(), name='user_video'),
    path('video/<int:video_pk>', VideoView.as_view(), name='video'),
    path('player/<int:video_pk>', PlayerStreamView.as_view(), name='player'),
    path('add/', CreateVideoView.as_view(), name='add_video')
]
