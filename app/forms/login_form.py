from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter username here', 'pattern': '.*\S+.*'}), required=True, strip=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password here', 'pattern': '.*\S+.*'}), required=True, strip=False)

    class Meta:
        model = User
        fields = ['username', 'password']
