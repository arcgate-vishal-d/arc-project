from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .all_questions import AllQuestions


class ImageMultipleChoiceQuestions(AbstractTable):
    question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=1000)
    answer_key = models.CharField(max_length=500)
    optionA = models.CharField(max_length=500)
    optionB = models.CharField(max_length=500)
    optionC = models.CharField(max_length=500)
    optionD = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "image_multiple_choice_questions"
