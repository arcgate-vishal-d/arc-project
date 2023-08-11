from django import forms
from django.forms import ModelForm
from app.models import SubjectiveQuestions, Subjects, PassageInstructionContents
from parsley.decorators import parsleyfy


@parsleyfy
class SubjectiveQuestionForm(ModelForm):
    question_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder':'Enter Question',
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '500',
        'data-parsley-maxlength-message': 'This field can have 500 characters maximum'
    }))
    answer_key = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder':'Enter Answer Key',
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '250',
        'data-parsley-maxlength-message': 'This field can have 250 characters maximum'
    }))
    instructions = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder':'Enter Instruction',
        "data-parsley-required": "true",
        'data-parsley-trigger': 'keyup',
        'data-parsley-maxlength': '100',
        'data-parsley-maxlength-message': 'This field can have 100 characters maximum'
    }))
    subjects = forms.ModelChoiceField(empty_label='--Please Search Subject---',label="Subject", 
                                      queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'data-placeholder':'Enter Subject',
        "data-parsley-required": "true",
        'style': "padding: 2px;",
    }))
    
    passage = forms.ModelChoiceField(required=False,empty_label='--Please Search Passage (Optional)---',label="Passage",
                                     queryset=PassageInstructionContents.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        'data-placeholder':'Enter Passage(Optional)',
        "data-parsley-required": "false",
        'style': "padding: 2px;",
    }))
    
    class Meta:
        model = SubjectiveQuestions
        fields = ['question_id','question_title','answer_key','instructions','subjects','passage']
        
        
@parsleyfy
class SearchSubjectiveQuestions(ModelForm):
   question_id = forms.ModelChoiceField(required=False, label="Subject", empty_label='--Please Select Subject---', 
                                        queryset=Subjects.objects.all(), widget=forms.Select(attrs={
        'class': "form-control",
        "data-parsley-required": "true",
        'style': "padding: 2px;",
    }))
   question_title = forms.CharField(widget=forms.TextInput(attrs={
       'class':"form-control",
       'placeholder':'Enter Question',
       'id':"searchquestion",
   }),required=False)
   
   class Meta:
       model = SubjectiveQuestions
       fields = ['question_id','question_title']
