from django.db import models
from django.contrib.auth.models import User

from .candidate import CandidateDetails
from .abstracttable import AbstractTable


class PersonalInterviewMap(AbstractTable):
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    interviewee = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)

    class Meta:
        db_table = "personal_interview_mapping"
