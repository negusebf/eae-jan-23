from django.db import models
from django.utils import timezone
from django.urls import reverse
from embed_video.fields import EmbedVideoField

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


class HomeView(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    link = EmbedVideoField()
    image = models.ImageField(upload_to='img', blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    # Because there are six dispaly rows choose one to fit in
    display_row = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.title


class Trending(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title



class HomeBaseText(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class PostsPage(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    top_cover_image = models.ImageField(upload_to='post_page_top_cover')
    created_at = models.DateTimeField(default=timezone.now)

    video_tag_image = models.ImageField(upload_to='post_page_top_cover')
    video_tag_title = models.CharField(max_length=200)
    video_tag_text = models.TextField()

    blog_article_tag_image = models.ImageField(upload_to='post_page_top_cover')
    blog_article_tag_title = models.CharField(max_length=200)
    blog_article_tag_text = models.TextField()


    def __str__(self):
        return self.title
        

class AboutVideo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='post_page_top_cover')
    created_at = models.DateTimeField(default=timezone.now)
    local_video_file = models.FileField(upload_to='about', blank=False, default="")


    def __str__(self):
        return self.title

class EmailSubscriptions(models.Model):
    subscriber_email = models.EmailField(max_length=255)
    is_subscriber_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subscriber_email


class FeedBackSubmission(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class ManualAdsManager(models.Model):
    ad_cat = [
    ('side', 'Side (Must be 360 by 370)'),
    ('bottom', 'Bottom (Must be 1260 by 370)'),
    ]
    ad_title = models.CharField(max_length=255)
    ad = models.ImageField(upload_to='img/manual_ads', blank=False) # Image should be 360*370
    ad_link = models.URLField(blank=False)
    ad_category = models.CharField(max_length=255, choices=ad_cat)

    added_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ad_title


