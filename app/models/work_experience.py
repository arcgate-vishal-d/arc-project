import datetime
from django.db import models

from .abstracttable import AbstractTable
from .candidate import CandidateDetails


class CandidateWorkExperience(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    joining_date = models.DateField(null=True)
    reliving_date = models.DateField(null=True)
    reason_of_leaving = models.CharField(max_length=500, null=True)
    last_salary = models.FloatField(null=True)

    class Meta:
        db_table = "candidate_work_experience"
