from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = "Email Address"
        self.fields['address'].label = "Address"
        self.fields['password2'].label = "Confirm Password"



class UserEditForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = ""    ################## Set the password change link to empty to setup your own
            password.label = ""        ################## Set the password change link to empty to setup your own

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'address']




class deleteProfileForm(UserChangeForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(
        label=("Confirm password:"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Enter your username"
        # password = self.fields.get('password')
        # if password:
        #     password.help_text = ""    ################## Set the password change link to empty to setup your own
        #     password.label = ""        ################## Set the password change link to empty to setup your own

    class Meta:
        model = get_user_model()
        fields = ['username']




##################3 Password Handler ##########################
class PasswordResetForm(PasswordResetForm):
    class Meta:
        fields = ('email')
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Enter email used to create the account'
        # Remember to copy how to write widgets and replace the placeholder attribute
        


##################3 Password Handler ##########################