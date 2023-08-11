from django import forms
from django.forms import ModelForm

from parsley.decorators import parsleyfy
from app.models import (MultipleChoiceQuestions, Subjects,
                        PassageInstructionContents, PassageInstructionContents)


@parsleyfy
class MultipleChoiceQuestionForm(ModelForm):

    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_title",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    optionA = forms.CharField(label="Option A", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_optionA",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionB = forms.CharField(label="Option B", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_optionB",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionC = forms.CharField(label="Option C", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_optionC",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    optionD = forms.CharField(label="Option D", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_optionD",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all(), label="Subject", 
        widget=forms.Select(attrs={
            'class': "form-control",
            'id': "MCQ_subject",
            "data-parsley-required": "true",
            'style': "padding: 0px;",
    }))
    passage = forms.ModelChoiceField(required=False, empty_label="Please select passage (optional)",
        queryset=PassageInstructionContents.objects.all(), label="Passage", widget=forms.Select(attrs={
            'class': "form-control",
            'id': "MCQ_passage",
            "data-parsley-required": "false",
            'style': "padding: 0px;",
    }))

    class Meta:
        model = MultipleChoiceQuestions
        fields = ['question_title', 'answer_key',
                  'optionA', 'optionB', 'optionC', 'optionD']


@parsleyfy
class MCQSearchForm(ModelForm):
    question_title = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "MCQ_title_search",
        "data-parsley-required": "true"
    }))
    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all(), required=False,
        empty_label="Please select subject",label="Subject", widget=forms.Select(attrs={
            'class': "form-control",
            'id': "MCQ_subject_search",
            "data-parsley-required": "true",
            'style': "padding: 0px;",
    }))

    class Meta:
        model = MultipleChoiceQuestions
        fields = ["question_title", "question_id"]
