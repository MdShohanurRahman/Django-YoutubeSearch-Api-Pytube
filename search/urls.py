from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/video', views.download_video, name='download_video'),
    path('download/audio', views.download_audio, name='download_audio'),
    path('download/playlists', views.download_playlist, name='download_playlist'),
]