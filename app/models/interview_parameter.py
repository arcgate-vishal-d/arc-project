from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable

class InterviewParameter(AbstractTable):
    parameter = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "interview_parameter"

    def __str__(self):
        return self.parameter
