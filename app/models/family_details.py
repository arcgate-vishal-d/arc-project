import datetime
from django.db import models

from .abstracttable import AbstractTable
from .candidate import CandidateDetails


RELATION = [
    ('FATHER', 'Father'),
    ('MOTHER', 'Mother'),
    ('BROTHER', 'Brother'),
    ('SISTER', 'Sister'),
    ('SPOUSE', 'Spouse')
]

OCCUPATION = [
    ('BUSINESS', 'Business'),
    ('GOVT EMPLOYEE', 'Govt. Employee'),
    ('NOT EMPLOYED', 'Not Employed'),
    ('STUDENT', 'Student'),
    ('PVT EMPLOYEE', 'Private Employee'),
    ('HOUSEWIFE', 'Housewife')
]


class CandidateFamilyDetails(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    relation = models.CharField(max_length=7, choices=RELATION, blank=True)
    occupation = models.CharField(
        max_length=100, choices=OCCUPATION, blank=True)
    dependent = models.BooleanField(blank=True)

    class Meta:
        db_table = "candidate_family_details"
