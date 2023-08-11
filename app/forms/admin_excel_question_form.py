from django import forms
from django.forms import ModelForm

from parsley.decorators import parsleyfy
from app.models import (ExcelQuestions)


@parsleyfy
class ExcelQuestionForm(ModelForm):

    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "excel_title",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        'class': "form-control",
        "style": "height:150px; width:425px",
        'id': "excel_description",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))

    class Meta:
        model = ExcelQuestions
        fields = ["question_title", "description"]


@parsleyfy
class ExcelImageForm(ModelForm):

    screenshot = forms.ImageField(label="Upload Image", widget=forms.FileInput(attrs={
        'id': "exel_image_upload",
        'data-parsley-max-file-size': "1000",
        'data-parsley-fileextension': 'jpeg,jpg,png',
        'multiple': "multiple",
    }))

    class Meta:
        model = ExcelQuestions
        fields = ["screenshot"]
