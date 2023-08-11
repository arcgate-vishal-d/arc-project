from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy
from app.utility import constants
from app import models

@parsleyfy
class PaperSearchForm(ModelForm):
   
    paper_sets = forms.ModelChoiceField(label="Papers sets",empty_label='--Please Select Paper Set---', required=False, queryset=models.PaperSetupDescription.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': "margin-bottom: 15px;",
        'style': "padding: 0px;",

    }))
    test_levels = forms.ModelChoiceField(label="Test levels", empty_label='--Please Select Test Level---', required=False, queryset=models.TestLevels.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': "padding: 0px;",


    }))

    class Meta:
        model = models.PaperSetupDescription
        fields = ['paper_sets', 'test_levels']
