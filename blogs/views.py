from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from blogs.models import Post, Comment
from django.utils import timezone
from blogs.forms import PostForm, CommentForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


from .models import User


per_page = 2

class PostListView(ListView):
    paginate_by = per_page
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    #login_url = 'accounts/login/'
    #redirect_field_name = 'blogs/post_detail.html'

    form_class = PostForm

    model = Post

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UpdateView):
    #login_url = 'accounts/login/'
    #redirect_field_name = 'blogs/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    #login_url = 'accounts/login/'
    #redirect_field_name = 'blogs/post_draft_list.html'

    paginate_by = per_page
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, created_by=User(self.request.user.pk)).order_by('-created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:post_list')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blogs:post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.created_by = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blogs:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogs/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blogs:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blogs:post_detail', pk=post_pk)


# @login_required
# def PostsByYouOnly(request):

#     your_post = Post.objects.order_by('-created_date')

#     your_post = Paginator(your_post, paginator)
#     page = request.GET.get('page')
#     your_post = your_post.get_page(page)

#     return render(request, 'blogs/post_list.html', {'your_post': your_post})
class PostsByYouOnly(ListView):
    paginate_by = per_page
    model = Post

    def get_queryset(self):
        return Post.objects.filter(created_date__lte=timezone.now(), created_by=User(self.request.user.pk)).order_by('-created_date')


# @login_required
# def PostsPublishedByYouOnly(request):

#     your_published_post = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

#     your_published_post = Paginator(your_published_post, paginator)
#     page = request.GET.get('page')
#     your_published_post = your_published_post.get_page(page)

#     return render(request, 'blogs/post_list.html', {'your_published_post': your_published_post})
class PostsPublishedByYouOnly(ListView):
    paginate_by = per_page
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=False, created_by=User(self.request.user.pk)).order_by('-published_date')


def BlogSearch(request):

    context = {}

    if request.method == 'POST':
        search_value = request.POST['search']
        
        blog_search_result = Post.objects.filter(title__icontains=search_value, published_date__isnull=False).order_by('-published_date')
                
        found = len(blog_search_result)

        paginator = Paginator(blog_search_result, 100) #per_page) # Remember to include page number e.g. , 6
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
        'page_obj': page_obj, 
        'found': found
        }
        return render(request, 'blogs/post_list.html', context)
    
    # return render(request, 'blogs/post_list.html', context)

# class BlogSearch(ListView):
#     def get_queryset(self):
#         return Post.objects.filter(title__icontains=self.request.POST['search_value'], published_date__isnull=False).order_by('-published_date')
    

                
            


