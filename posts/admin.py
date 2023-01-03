from django.contrib import admin
from posts.models import LinkedVideos, LocalVideos
from embed_video.admin import AdminVideoMixin

# Register your models here.

class ContentListing(AdminVideoMixin, admin.ModelAdmin):
	list_display = ('author', 'title', 'published_date', 'post_label')
	list_display_links = ('author', 'title')
	list_filter = ('author', 'title', 'post_label')
	list_per_page = 18
	#list_editable = ()
	search_fields = ('title', )



admin.site.register(LinkedVideos, ContentListing)

admin.site.register(LocalVideos, ContentListing)
