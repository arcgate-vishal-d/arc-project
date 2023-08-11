from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .all_questions import AllQuestions


class MultipleImageChoiceQuestion(AbstractTable):
    question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question_title = models.CharField(max_length=1000)
    answer_key = models.ImageField(upload_to="images/")
    optionA = models.ImageField(upload_to="images/")
    optionB = models.ImageField(upload_to="images/")
    optionC = models.ImageField(upload_to="images/")
    optionD = models.ImageField(upload_to="images/")
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "multiple_image_choice_question"
