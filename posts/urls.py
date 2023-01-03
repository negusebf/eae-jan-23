from django.urls import re_path as url
from . import views
from django.urls import path
from management.models import HomeView

app_name = "posts"

urlpatterns = [
    path("", views.Posts, name="posts"),
    path("videos/", views.Videos, name="videos"),

    path("videos/linked_video_player/<id>", views.LinkedVideoPlayer, name="linked_video_player"),
    path("videos/local_video_player/<id>", views.LocalVideoPlayer, name="local_video_player"),

    path("videos/search/linked/", views.VideosSearch, name="video_search"),
    # path("videos/search/linked/", views.LinkedVideosSearch, name="linked_video_search"),
    # path("videos/search/local/", views.LocalVideosSearch, name="local_video_search"),
    path('videos/txt_edit/<id>', views.VideosTxtEditor, name="text_editor"),
]