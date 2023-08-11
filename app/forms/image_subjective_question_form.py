from django import forms
from django.forms import ModelForm
from django.db.models.fields import BLANK_CHOICE_DASH

from app .models import Subjects, ImageBasedSubjectiveQuestions

from parsley.decorators import parsleyfy


@parsleyfy
class ImageSubjectiveQuestionForm(ModelForm):
    question_title = forms.CharField(label="Question", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "IBSQ_question",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    answer_key = forms.CharField(label="Answer", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "IBSQ_answer_key",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    image_upload = forms.ImageField(label="Upload Image", widget=forms.FileInput(attrs={
        'id': "IBSQ_image_upload",
        'data-parsley-max-file-size': "500",
        'data-parsley-fileextension': 'jpeg,jpg,png',
        'multiple': "multiple",

    }))
    subjects = forms.ModelChoiceField(label="Select Subject", queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'id': "IBSQ_subject",
        "data-parsley-required": "true",
        'style': "padding:1px",
    }))

    class Meta:
        model = ImageBasedSubjectiveQuestions
        fields = ['question_title', 'answer_key', 'image_upload', 'subjects']


class ImgSubjectiveQueSearchForm(ModelForm):

    question = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "IBSQ_question_search",
    }), required=False)

    subjects = forms.ModelChoiceField(label="Subject", required=False, queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'id': "IBSQ_subject_search",
        'style': "padding: 0px;",

    }))

    class Meta:
        model = ImageBasedSubjectiveQuestions
        fields = ['subjects', 'question']
