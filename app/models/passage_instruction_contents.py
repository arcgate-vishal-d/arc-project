from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .all_questions import AllQuestions


STATUS = (
    ('passage', "passage"),
    ('instruction', "instruction"),
    ('typing', "typing")
)

class PassageInstructionContents(AbstractTable):
    question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    types = models.CharField(
        choices=STATUS, default='instruction', max_length=50)
    question_title = models.CharField(max_length=5000)
    description = models.TextField()
    status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.question_title} -({self.types})"

    class Meta:
        db_table = "passage_instruction_contents"
