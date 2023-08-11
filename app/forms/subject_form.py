from django import forms
from django.forms import ModelForm
from app.models.subjects import Subjects

from parsley.decorators import parsleyfy


@parsleyfy
class SubjectForm(ModelForm):
    subject = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder':"Word Limit : 50 Characters",
               'Id': "id_subject",
               "data-parsley-required": "true",
               "data-parsley-pattern":"^[a-zA-Z][a-zA-Z -/]+$",
               "data-parsley-pattern-message":"This field should start with a letter and doesn't accept digits"
               }))

    class Meta:
        model = Subjects
        fields = ['subject']
