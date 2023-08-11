from django.db import models
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .candidate import CandidateDetails
from .interview_parameter import InterviewParameter

class PersonalInterview(AbstractTable):
    interviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    parameter = models.ForeignKey(InterviewParameter, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=1000)

    class Meta:
        db_table = "personal_interview"
