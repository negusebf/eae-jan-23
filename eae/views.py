from django.views.generic import TemplateView
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.core.mail import EmailMessage, send_mail, send_mass_mail, EmailMultiAlternatives

from management.models import HomeView, Trending, HomeBaseText, AboutVideo, EmailSubscriptions, FeedBackSubmission, ManualAdsManager

from blogs.models import Post
from posts.models import LinkedVideos, LocalVideos
from django.core.mail import send_mail



class TestPage(TemplateView):
	template_name = 'visits/test.html'

class ThanksPage(TemplateView):
	template_name = 'visits/thanks.html'



def HomePage(request):
    listings_1 = LinkedVideos.objects.order_by('-published_date')[0:1]
    listings_2 = LinkedVideos.objects.order_by('-published_date')[1:4]
    listings_3 = LinkedVideos.objects.order_by('-published_date')[0:2]
    listings_4 = LinkedVideos.objects.order_by('-published_date')[2:8]
    listings_5 = LocalVideos.objects.order_by('-published_date')[0:6]
    listings_6 = Post.objects.order_by('-published_date')[0:6]
    video_listings = AboutVideo.objects.order_by('-created_at')[0:1]
    trending_listings = Trending.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:4]
    home_base_text = HomeBaseText.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[0:1]
    datetime_filter_month = LinkedVideos.objects.filter(published_date__lte=timezone.now().date())[0:2]
    datetime_filter_month1 = LinkedVideos.objects.filter(published_date__lte=timezone.now().date())[2:2+(30-int(timezone.datetime.now().date().day))]
    datetime_filter_year = LinkedVideos.objects.filter(published_date__lte=timezone.now().date())[0:2]
    datetime_filter_year1 = LinkedVideos.objects.filter(published_date__lte=timezone.now().date())[2:2+(364-int(timezone.datetime.now().date().day))]
    
    side_ad = ManualAdsManager.objects.filter(ad_category='side').order_by('-added_date')[0:1]
    bottom_ad = ManualAdsManager.objects.filter(ad_category='bottom').order_by('-added_date')[0:1]

    context={
    'listings_1': listings_1,
    'listings_2': listings_2,
    'listings_3': listings_3,
    'listings_4': listings_4,
    'listings_5': listings_5,
    'listings_6': listings_6,
    'video_listings': video_listings,
    'trending_listings': trending_listings,
    'home_base_text': home_base_text,
    'datetime_filter_month': datetime_filter_month,
    'datetime_filter_month1': datetime_filter_month1,
    'datetime_filter_year': datetime_filter_year,
    'datetime_filter_year1': datetime_filter_year1,
    'side_ad': side_ad,
    'bottom_ad': bottom_ad,
    }
    return render(request, 'index.html', context)



def contact(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact/contact.html',
        {
            'location':'Asmara, Eritrea',
            'phone': '+291178704',
            'box':'P.O.Box: 4106',
            'year':datetime.now().year,
            'email':'negusebf12@gmail.com',
            'message':'this is Negusse Berhane, the CEO of ForesightEritrea. ForesightEritrea is a non-profit organization dedicated for those with stronger desire to learn machine learning and deep learning models, share their experiences and post new ideas on the site. Thank you for visiting',
        }
    )


def single_post(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'eae/single-post.html',
        {
            'location':'Asmara, Eritrea',
            'site': 'https://www.resinv.com',
            'box':'P.O.Box: 4106',
            'year':datetime.now().year,
            'email':'negusebf12@gmail.com',
            'message':'this is Negusse Berhane, the CEO of ForesightEritrea. ForesightEritrea is a non-profit organization dedicated for those with stronger desire to learn machine learning and deep learning models, share their experiences and post new ideas on the site. Thank you for visiting',
        }
    )


def AboutVideoPlayer(request, id):

    local_video_single = get_object_or_404(AboutVideo, pk=id)

    context = {
    'local_video_single': local_video_single
    }

    return render(request, 'posts/local_video_player.html', context)


class CategoricalViewsBlogs(ListView):
    paginate_by = 6
    model = Post

    def get_queryset(self):
        #self.publisher = get_object_or_404(Post, post_label=self.kwargs['post_label'])
        return Post.objects.filter(post_label=self.kwargs['post_label'], published_date__isnull=False).order_by('-published_date')



class CategoricalViewsLinkedVideos(ListView):
    paginate_by = 6
    model = LinkedVideos
    template_name = 'posts/videos.html'
    context_object_name = 'cat_lin_vid'

    def get_queryset(self):
        #self.publisher = get_object_or_404(Post, post_label=self.kwargs['post_label'])
        return LinkedVideos.objects.filter(post_label=self.kwargs['post_label'], published_date__isnull=False).order_by('-published_date')



class CategoricalViewsLocalVideos(ListView):
    paginate_by = 6
    model = LocalVideos
    template_name = 'posts/videos.html'
    context_object_name = 'cat_loc_vid'

    def get_queryset(self):
        #self.publisher = get_object_or_404(Post, post_label=self.kwargs['post_label'])
        return LocalVideos.objects.filter(post_label=self.kwargs['post_label'], published_date__isnull=False).order_by('-published_date')



def EmailSubscriptionView(request):
    prev_emails = EmailSubscriptions.objects.all()
    flag = True
    context = {'message': ''}

    if request.method == 'POST':
        email = request.POST['sub_email']
        for i in prev_emails:
            if i.subscriber_email == email:
                flag = False

        if flag == True:
            sub_email = EmailSubscriptions(subscriber_email = email)
            # Now send the user an email of confirmation
            send_mail(
                'foresight-Eritrea: Email Subscription',
                'Hi '+str(sub_email).split("@")[0]+', Thank you for subscribing to foresight-ERITREA newsletter. You will now receive daily updates on our web archive. Also feel free to contact us for any kind of help or feedback. If you wish to unsubscribe, please do so by going to your settings page.',
                'resinv.pos@gmail.com',
                [sub_email,'negusebf12@gmail.com'],
                fail_silently=False
            )
            # After sending now save the reciepients
            sub_email.save()
            context = {'message': 1}

        else:
            context = {'message': 2}

        return render(request, 'visits/thanks.html', context)



def FeedBackSubmissionView(request):
    prev_emails = FeedBackSubmission.objects.all()
    flag = True
    context = {'message': ''}

    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        for i in prev_emails:
            if i.email == email:
                flag = False

        if flag == True:
            feedback = FeedBackSubmission(full_name = full_name, email = email, subject = subject, message = message)
            feedback.save()
            context = {'message': 1}

        else:
            context = {'message': 2}

        return render(request, 'contact/contact.html', context)