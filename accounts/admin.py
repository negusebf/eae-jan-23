from django.contrib import admin
from accounts.models import User
# Register your models here.

class UsersListing(admin.ModelAdmin):
	list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_staff', 'is_active')


admin.site.register(User, UsersListing)
