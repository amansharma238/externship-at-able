from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import SalesUser


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter First Name'}
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Last Name'}
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter email address'}
    ))
    password1 = forms.Field(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password'}))
    password2 = forms.Field(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,12}$', message="Phone number must be entered in the format: '9999999999'. Up to 12 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=12, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Phone Number'}
    ))

    class Meta:
        model = SalesUser
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'password1', 'password2')


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = SalesUser
        fields = ('email', 'phone_number', 'user_type',
                  'manager_id', 'user_bio', 'is_approved')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
