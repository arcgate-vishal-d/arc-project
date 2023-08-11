from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy
from app.utility import constants

USER_ROLE = [
    ("2", "Admin"),
    ("3", "Interviewer"),
]


@parsleyfy
class UserSettingsForm(ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "userSettingUsername",
        "data-parsley-required": "true"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "userSettingEmail",
        "data-parsley-required": "true",
        "data-parsley-pattern-message": "This is not an arcgate email.",
        'pattern': '(^[A-Za-z0-9._%+-]+@arcgate\.com$)',
    }))
    role = forms.ChoiceField(choices=BLANK_CHOICE_DASH + USER_ROLE, widget=forms.Select(attrs={
        'class': "form-control",
        'id': "userSettingRole",
        "data-parsley-required": "true"
    }))
    status = forms.ChoiceField(choices=BLANK_CHOICE_DASH + constants.STATUS, widget=forms.Select(attrs={
        'class': "form-control",
        'id': "userSettingStatus",
        "data-parsley-required": "true"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'status']


@parsleyfy
class SearchForm(ModelForm):
    USER_ROLE = [
        ("1", "Administrator"),
        ("2", "Admin"),
        ("3", "Interviewer"),
    ]

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=False,)
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=False,)
    role = forms.ChoiceField(choices=BLANK_CHOICE_DASH + USER_ROLE, widget=forms.Select(attrs={
        'class': "form-control",
    }), required=False,)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']
