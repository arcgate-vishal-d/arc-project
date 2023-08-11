from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .passage_instruction_contents import PassageInstructionContents
from .all_questions import AllQuestions


class SubjectiveQuestions(AbstractTable):
    question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=1000)
    instructions = models.CharField(max_length=1000, null=True, blank= True)
    answer_key = models.CharField(max_length=1000)
    passage = models.ForeignKey(PassageInstructionContents, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = "subjective_questions"
