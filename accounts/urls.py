from django.urls import re_path as url
from accounts import views
# from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    url('login/', views.Login.as_view(), name='login'),
    url('logout/', views.Logout.as_view(), name='logout'),
    url('signup/', views.SignUp.as_view(), name='signup'),
    url('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    url('password_reset/', views.PasswordReseterView.as_view(), name='password_reset'),
    url('password_reset/done/', views.PasswordReseterDoneView.as_view(), name='password_reset_done'),
    url('reset/<uidb64>/<token>/', views.PasswordReseterConfirmView.as_view(), name='password_reset_confirm'),
    url('reset/done/', views.PasswordReseterCompleteView.as_view(), name='password_reset_complete'),
    url('password_change/', views.PasswordChangerView.as_view(), name='password_change'),
    url('password_change/done/', views.PasswordChangerDoneView.as_view(), name='password_change_done'),
    url('user_edit/', views.UserEditView.as_view(), name='user_edit'),
    url('change_password/', views.change_password, name='change_password'),
    url('deleteprofile', views.deleteProfile, name='deleteprofile'),
]
