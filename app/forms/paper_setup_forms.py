from django import forms
from django.forms import ModelForm
from django.db.models.fields import BLANK_CHOICE_DASH

from app .models import Grades

from parsley.decorators import parsleyfy


@parsleyfy
class GradeForms(ModelForm):
    from_field = forms.FloatField(label="From(%)", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "gradeFrom",
        "data-parsley-required": "true",
        "data-parsley-range": "[0, 99]",
        "data-parsley-invalid_grade": "true",
        "data-parsley-grade-format": "",
        "data-parsley-invalid_grade-message": "Invalid grade formate"

    }))
    to_field = forms.FloatField(label="To(%)", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "gradeTo",
        "data-parsley-required": "true",
        "data-parsley-range": "[1, 101]",
        "data-parsley-invalid_grade": "true",
        "data-parsley-grade-format": "",
        "data-parsley-invalid_grade-message": "Invalid grade formate"

    }))
    grade = forms.CharField(label="Grade", widget=forms.TextInput(attrs={
        'class': "form-control",
        'id': "gradeTitle",
        "data-parsley-required": "true",
        "data-parsley-invalid_grade-message": "Grade title should be unique."
    }))

    class Meta:
        model = Grades
        fields = ['grade_from', 'grade_to', 'grade']
