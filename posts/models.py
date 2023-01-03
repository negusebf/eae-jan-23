from django.db import models
from django.utils import timezone
from django.urls import reverse
from embed_video.fields import EmbedVideoField

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


class LinkedVideos(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    link = EmbedVideoField()
    image = models.ImageField(upload_to='img', blank=False)
    published_date = models.DateTimeField(default=timezone.now)

    post_label_choices = [
    ('er_hist', 'Eritrean Histories'),
    ('er_cult', 'Eritrean Culture'),
    ('er_polt', 'Politics'),
    ('er_peop', 'People'),
    ('er_tech', 'Technology'),
    ('other', 'Other'),
    ]
    post_label = models.CharField(max_length=200, null=True, blank=True, choices=post_label_choices)

    def __str__(self):
        return self.title


class LocalVideos(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    local_video_file = models.FileField(upload_to='local_videos', blank=False, default="")
    image = models.ImageField(upload_to='img', blank=True)
    published_date = models.DateTimeField(default=timezone.now)

    post_label_choices = [
    ('er_hist', 'Eritrean Histories'),
    ('er_cult', 'Eritrean Culture'),
    ('er_polt', 'Politics'),
    ('er_peop', 'People'),
    ('er_tech', 'Technology'),
    ('other', 'Other'),
    ]
    post_label = models.CharField(max_length=200, null=True, blank=True, choices=post_label_choices)

    def __str__(self):
        return self.title
