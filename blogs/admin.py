from django.contrib import admin
from blogs.models import Post, Comment

# Register your models here.

class PostContentListing(admin.ModelAdmin):
	list_display = ('created_by', 'author', 'title', 'published_date', 'created_date', 'post_label')
	list_display_links = ('created_by', 'title', 'author')
	list_filter = ('created_by', 'author', 'title', 'post_label')
	list_per_page = 18
	#list_editable = ()
	search_fields = ('created_by', 'title', 'author')


class CommentContentListing(admin.ModelAdmin):
	list_display = ('created_by', 'created_date', 'approved_comments', 'text', 'post')
	list_display_links = ('created_by',)
	list_filter = ('created_by','approved_comments')
	list_per_page = 18
	#list_editable = ()
	search_fields = ('created_by', 'text')

admin.site.register(Post, PostContentListing)
admin.site.register(Comment, CommentContentListing)
