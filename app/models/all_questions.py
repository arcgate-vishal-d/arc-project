from django.db import models

from .abstracttable import AbstractTable
from .subjects import Subjects


class AllQuestions(AbstractTable):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

    class Meta:
        db_table = "all_questions"
