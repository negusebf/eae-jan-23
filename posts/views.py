from django.views.generic import TemplateView
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import PostsPage
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import LinkedVideos, LocalVideos
from management.models import ManualAdsManager

# Create your views here.

per_page = 3

def Posts(request):
    cover_page = PostsPage.objects.order_by('-created_at')[0:1]
    context = {'cover_page':cover_page}
    return render(request, 'posts/posts.html', context)




def Videos(request):
    
    linked_video_listings = LinkedVideos.objects.order_by('-published_date')
    local_video_listings = LocalVideos.objects.order_by('-published_date')

    paginator1 = Paginator(linked_video_listings, per_page)
    paginator2 = Paginator(local_video_listings, per_page)

    page = request.GET.get('page')

    paged_listing1 = paginator1.get_page(page)
    paged_listing2 = paginator2.get_page(page)

    side_ad = ManualAdsManager.objects.filter(ad_category='side').order_by('-added_date')[0:1]
    bottom_ad = ManualAdsManager.objects.filter(ad_category='bottom').order_by('-added_date')[0:1]
 
    context = {
                'linked_video_listings':paged_listing1,
                'local_video_listings': paged_listing2,
                'side_ad': side_ad,
                'bottom_ad': bottom_ad
                }

    return render(request, 'posts/videos.html', context)


@login_required
def LinkedVideoPlayer(request, id):

    linked_video_single = get_object_or_404(LinkedVideos, pk=id)
    linked_video_single_url = str(linked_video_single.link)
    linked_video_single_url = linked_video_single_url[:20] + linked_video_single_url[26:]
    linked_video_single_url = linked_video_single_url[:15] + linked_video_single_url[19:]
    linked_video_single_url = linked_video_single_url[:13] + ".be" + linked_video_single_url[15:]
    print(linked_video_single_url)
    sidebar_related_videos = LinkedVideos.objects.filter(post_label=linked_video_single.post_label).order_by('-published_date')
    side_ad = ManualAdsManager.objects.filter(ad_category='side').order_by('-added_date')[0:1]
    bottom_ad = ManualAdsManager.objects.filter(ad_category='bottom').order_by('-added_date')[0:1]

    context = {
    'linked_video_single': linked_video_single,
    'side_ad': side_ad,
    'bottom_ad': bottom_ad,
    'sidebar_related_videos': sidebar_related_videos,
    'linked_video_single_url': linked_video_single_url
    }

    return render(request, 'posts/linked_video_player.html', context)

@login_required
def LocalVideoPlayer(request, id):

    local_video_single = get_object_or_404(LocalVideos, pk=id)
    sidebar_related_videos = LocalVideos.objects.filter(post_label=local_video_single.post_label).order_by('-published_date')
    side_ad = ManualAdsManager.objects.filter(ad_category='side').order_by('-added_date')[0:1]
    bottom_ad = ManualAdsManager.objects.filter(ad_category='bottom').order_by('-added_date')[0:1]

    context = {
    'local_video_single': local_video_single,
    'side_ad': side_ad,
    'bottom_ad': bottom_ad,
    'sidebar_related_videos': sidebar_related_videos
    }

    return render(request, 'posts/local_video_player.html', context)


'''


def LinkedVideosSearch(request):
    search_value = request.POST['search']
    flag = 'flag'
    linked_search_result = LinkedVideos.objects.filter(title__icontains=search_value).order_by('-published_date')
    
    found = len(linked_search_result)

    paginator = Paginator(linked_search_result, 6)
    page = request.GET.get('page')
    linked_paged_search_listing = paginator.get_page(page)

    context = {
    'linked_paged_search_listing': linked_paged_search_listing, 
    'flag': flag, 
    'found': found
    }
    return render(request, 'posts/videos.html', context)



def LocalVideosSearch(request):
    search_value = request.POST['search']
    flag = 'flag'
    local_search_result = LinkedVideos.objects.filter(title__icontains=search_value).order_by('-published_date')
    
    found = len(local_search_result)

    paginator = Paginator(local_search_result, 6)
    page = request.GET.get('page')
    local_paged_search_listing = paginator.get_page(page)

    context = {
    'local_paged_search_listing': local_paged_search_listing, 
    'flag': flag, 
    'found': found
    }
    return render(request, 'posts/videos.html', context)


'''



def VideosSearch(request):

    flag = "flag"

    if request.method == 'POST':
        search_value = request.POST['search']
        video_type = request.POST['video_type']
        context = {}
        if video_type == 'linked':
                
            linked_search_result = LinkedVideos.objects.filter(title__icontains=search_value).order_by('-published_date')
                
            found = len(linked_search_result)

            paginator = Paginator(linked_search_result, int(found)+1) # Remember to include page number e.g. , 6
            page = request.GET.get('page')
            linked_paged_search_listing = paginator.get_page(page)

            context = {
            'linked_paged_search_listing': linked_paged_search_listing, 
            'flag': flag, 
            'found': found
            }

        elif video_type == 'local':
                
            local_search_result = LocalVideos.objects.filter(title__icontains=search_value).order_by('-published_date')

            found = len(local_search_result)

            paginator = Paginator(local_search_result, int(found)+1) # Remember to include page number e.g. , 6
            page = request.GET.get('page')
            local_paged_search_listing = paginator.get_page(page)

            context = {
            'local_paged_search_listing': local_paged_search_listing, 
            'flag': flag, 
            'found': found
            }

        return render(request, 'posts/videos.html', context)




def VideosTxtEditor(request, id):

    linked_video_single = get_object_or_404(LinkedVideos, pk=id)
    linked_video_single_url = str(linked_video_single.link)
    linked_video_single_url = linked_video_single_url[:20] + linked_video_single_url[26:]
    linked_video_single_url = linked_video_single_url[:15] + linked_video_single_url[19:]
    linked_video_single_url = linked_video_single_url[:13] + ".be" + linked_video_single_url[15:]
    sidebar_related_videos = LinkedVideos.objects.filter(post_label=linked_video_single.post_label).order_by('-published_date')
    side_ad = ManualAdsManager.objects.filter(ad_category='side').order_by('-added_date')[0:1]
    bottom_ad = ManualAdsManager.objects.filter(ad_category='bottom').order_by('-added_date')[0:1]

    context = {
    'linked_video_single': linked_video_single,
    'side_ad': side_ad,
    'bottom_ad': bottom_ad,
    'sidebar_related_videos': sidebar_related_videos,
    'linked_video_single_url': linked_video_single_url
    }

    if request.method == 'POST':
        txt = request.POST['txt_editor']
        print(txt)
        LinkedVideos.objects.filter(pk=id).update(text=txt)

    return render(request, 'posts/linked_video_player.html', context)

        
