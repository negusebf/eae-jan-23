"""simplesocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'eae'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage, name='home'),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("test/", views.TestPage.as_view(), name="test"),
    path("thanks/", views.ThanksPage.as_view(), name="thanks"),
    path("contact/", views.contact, name="contact"),
    path("posts/", include("posts.urls")),
    path("blogs/", include("blogs.urls")),
    path('about_video/<id>', views.AboutVideoPlayer, name='about_video'),
    path('ads/', include('ads.urls', namespace='adverts')),

    path("categories/videos/local/<post_label>", views.CategoricalViewsLocalVideos.as_view(), name="categorical_views_local_videos"),
    path("categories/videos/linked/<post_label>", views.CategoricalViewsLinkedVideos.as_view(), name="categorical_views_linked_videos"),
    path("categories/blogs/<post_label>", views.CategoricalViewsBlogs.as_view(), name="categorical_view_blogs"),
    path("email_subscribtion/", views.EmailSubscriptionView, name="email_subscription"),
    path("feed_back/", views.FeedBackSubmissionView, name="feedback_submission"),
]



if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
