from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy

from app .models import MultipleImageChoiceQuestion, Subjects


@parsleyfy
class MICQForms(ModelForm):

    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MICQ_title",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all(), label="Subject", widget=forms.Select(attrs={
        'class': "form-control",
        'id': "MICQ_subject",
        "data-parsley-required": "true",
        'style': "padding: 2px;",
    }))
    optionA = forms.ImageField(label="Option A", widget=forms.FileInput(attrs={
        'id': "MICQ_optionA",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,png,jpg',
    }))
    optionB = forms.ImageField(label="Option B", widget=forms.FileInput(attrs={
        'id': "MICQ_optionB",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,png,jpg',
    }))
    optionC = forms.ImageField(label="Option C", widget=forms.FileInput(attrs={
        'id': "MICQ_optionC",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,png,jpg',
    }))
    optionD = forms.ImageField(label="Option D", widget=forms.FileInput(attrs={
        'id': "MICQ_optionD",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,png,jpg',
    }))

    answer_key = forms.ImageField(label="Answer key",  widget=forms.FileInput(attrs={
        'class': "form-control",
        'id': "MICQ_answerkey",
        "data-parsley-required": "true"
    }))

    class Meta:
        model = MultipleImageChoiceQuestion
        fields = ['question_title', 'answer_key',
                  'optionA', 'optionB', 'optionC', 'optionD']


class MICQSearchForm(ModelForm):
    question_title = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=False)
    subject = forms.ModelChoiceField(label="Subject", empty_label="Search subject", required=False, queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': "padding: 0px;",
    }))

    class Meta:
        model = MultipleImageChoiceQuestion
        fields = ['question_title', 'subject']
