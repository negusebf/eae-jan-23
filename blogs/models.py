from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    blog_cover_image = models.ImageField(upload_to="img/blogs/", blank=False, null=False)
    post_quote = models.CharField(max_length=15, default="Quote", null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    post_label_choices = [
    ('er_hist', 'Eritrean Histories'),
    ('er_cult', 'Eritrean Culture'),
    ('er_polt', 'Politics'),
    ('er_peop', 'People'),
    ('er_tech', 'Technology'),
    ('other', 'Other'),
    ]
    post_label = models.CharField(max_length=200, null=True, blank=True, choices=post_label_choices)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        return reverse("blogs:post_detail", kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blogs.Post', related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('blogs:post_list')

    def __str__(self):
        return self.text
