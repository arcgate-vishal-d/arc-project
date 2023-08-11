from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy
from app.models import ImageMultipleChoiceQuestions, Subjects, PassageInstructionContents

from app.utility import constants


@parsleyfy
class ImageMcqSearchForm(ModelForm):
    question_title = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=False)
    subject = forms.ModelChoiceField(label="Subject", empty_label="Search subject", required=False, queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'style': "padding: 0px;",

    }))

    class Meta:
        model = ImageMultipleChoiceQuestions
        fields = ['question_title', 'subject']


@parsleyfy
class ImageMcqSettingForm(ModelForm):
    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_title",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    answer_key = forms.CharField(max_length=500, widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_answer_key",
        "data-parsley-required": "true"
    }))
    optionA = forms.CharField(label="Option A", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_optionA",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionB = forms.CharField(label="Option B", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_optionB",
        "data-parsley-required": "true",
        "data-parsley-trigger": "keyup",
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionC = forms.CharField(label="Option C", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_optionC",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionD = forms.CharField(label="Option D", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "image_MCQ_optionD",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))

    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all(),label="Subject",widget=forms.Select(attrs={
        'class': "form-control",
        'id': "image_MCQ_subject",
        "data-parsley-required": "true",
        'style': "padding: 0px;",
        
    }))
    image_upload = forms.ImageField(label="Upload Image", widget=forms.FileInput(attrs={
        'id': "MCQ_image_upload",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,png,jpg',
     }))

    class Meta:
        model = ImageMultipleChoiceQuestions
        fields = ['question_title', 'answer_key', 'optionA', 'optionB','optionC','optionD', 'image_upload']
