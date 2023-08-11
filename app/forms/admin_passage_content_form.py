from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH

from parsley.decorators import parsleyfy
from app.models import PassageInstructionContents, Subjects
from app.utility import constants

TYPES = [
    ('passage', "passage"),
    ('instruction', "instruction"),
    ('typing', "typing")
]


@parsleyfy
class PassageContentSearchForm(ModelForm):
    types = forms.ChoiceField(choices=BLANK_CHOICE_DASH + TYPES, widget=forms.Select(attrs={
        'class': "form-control",
        'style': "padding: 0px;",
    }), required=False)
    question_title = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={
        'class': "form-control",
    }), required=False)

    class Meta:
        model = PassageInstructionContents
        fields = ['types', 'question_title']


@parsleyfy
class PassageSettingForm(ModelForm):
    types = forms.ChoiceField(choices=BLANK_CHOICE_DASH + TYPES, widget=forms.Select(attrs={
        'class': "form-control",
        'id': "passage_settings_types",
        "data-parsley-required": "true",
        'style': "padding: 0px;",
    }))
    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "passage_settings_title",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all(), label="Subject",
                                      widget=forms.Select(attrs={
                                          'class': "form-control",
                                          'id': "passage_content_subject",
                                          "data-parsley-required": "true",
                                          'style': "padding: 0px;",
                                      }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control",
        'id': "passage_settings_description",
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '5000',
        'data-parsley-maxlength-message': 'This field can have 5000 characters maximum'
    }))
    status = forms.ChoiceField(choices=BLANK_CHOICE_DASH + constants.STATUS, widget=forms.Select(attrs={
        'class': "form-control",
        'id': "passage_settings_status",
        "data-parsley-required": "true",
        'style': "padding: 0px;",
    }))

    class Meta:
        model = PassageInstructionContents
        fields = ['types', 'question_title',
                  'subjects', 'description', 'status']
