from django.shortcuts import render, redirect
# from accounts.models import User
from django.urls import reverse_lazy #from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, DeleteView
from django.contrib.auth import views
from . import forms
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.backends.base import SessionBase

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm




User = settings.AUTH_USER_MODEL


class SignUp(View):  ## But the inheritance should be UserCreationView
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True # Deactivate account till it is confirmed
            user.save()

            # current_site = get_current_site(request)
            # subject = 'Activate Your ForeSight-Eritrea Account'

            # message = render_to_string('accounts/account_activation_email.html', {
            #     'user': user,
            #     'protocol': 'https' if request.is_secure() else "http",
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            
            # user.email_user(subject, message)

            messages.success(request, ('We have sent you an email. Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})



class ActivateAccount(View):
     
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')




class UserEditView(UpdateView):
    form_class = forms.UserEditForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/edit_user_profile.html.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Your profile has been successfully updated!')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully changed!')
            # return redirect('home')
            return render(request, 'index.html', {'msg_edit_pass': 'Your password was successfully changed!'})
        else:
            return render(request, 'accounts/change_password.html', {'form': form, 'err_msg': 'Please correct the error above.'})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


from django.contrib.auth.hashers import make_password, check_password
from .models import User as u
def deleteProfile(request):
    username = request.user.username
    password = request.user.password
    form = forms.deleteProfileForm
    result = "Nothing happened"
    if username: ### Check if username is valid and logged-in
        if request.method == 'POST':
            userprofile = u.objects.get(username = username)
            # passprofile = u.objects.get(password = password)
            # print(userprofile)
            # print(passprofile)
            # print(username)
            # print(password)
            # print(str(request.POST['username']))
            # print(check_password(str(request.POST['password']), password))
            if (str(request.POST['username']) == str(userprofile)[1:]) and (check_password(str(request.POST['password']), password)):  #### Ommit the @ simbol
                userprofile.delete()
                context = {'result': 'Your profile has been successfully deleted!'}
                return render(request, 'index.html', context)
            else:
                context = {'err_result': 'You have entered incorrect username or password. Please try again!'}
                return render(request, 'accounts/delete_profile.html', context)
    else:
        context = {'result': 'Error: Username might have already been deleted!'}
        return render(request, 'accounts/delete_profile.html', context)

    context = {'form': form}

    return render(request, 'accounts/delete_profile.html', context)




    





class Login(views.LoginView):
    template_name = 'accounts/login.html'




class Logout(views.LogoutView):
    success_url = reverse_lazy('logout')






##################### Password Reset Handler ######################

class PasswordReseterView(views.PasswordResetView):
    form_class = forms.PasswordResetForm
    email_template_name = "accounts/password_reset_email.html"
    html_email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    template_name = 'accounts/password_reset.html'
    from_email = 'resinv.pos@gmail.com'


class PasswordReseterDoneView(views.PasswordResetDoneView):
    success_url = reverse_lazy('password_reset_done')
    template_name = "accounts/password_reset_done.html"


class PasswordReseterConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = "accounts/password_reset_confirm.html"


class PasswordReseterCompleteView(views.PasswordResetCompleteView):
    success_url = reverse_lazy('password_change_done')
    template_name = "accounts/password_reset_complete.html"

class PasswordChangerView(views.PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "accounts/password_change_form.html"


class PasswordChangerDoneView(views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"




##################### Password Reset Handler ######################