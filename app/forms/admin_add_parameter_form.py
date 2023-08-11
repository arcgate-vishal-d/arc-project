from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy
from app.models import InterviewParameter

from app.utility import constants


@parsleyfy
class AddParameterForm(ModelForm):
    parameter = forms.CharField (max_length= 30, widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=True)

    class Meta:
        model = InterviewParameter
        fields = ['parameter']
