import datetime
from django.db import models

from .abstracttable import AbstractTable
from .candidate import CandidateDetails


QUALIFICATION = [
    ('OTHER', 'other'),
    ('PG', 'Post Graduate'),
    ('UG', 'Under Graduate'),
    ('DIPLOMA', 'Diploma'),
    ('12', 'Higher Secondary'),
    ('10', 'Secondary')
]

DIVISION = [
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third')
]

MEDIUM = [
    ('E', 'English'),
    ('H', 'Hindi'),
    ('O', 'Others')
]


class CandidateEducationDetails(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    qualifications = models.CharField(
        max_length=24, choices=QUALIFICATION, null=True)
    education_details = models.CharField(max_length=500, blank=True)
    school_college = models.CharField(max_length=100, blank=True)
    board_university = models.CharField(max_length=100, blank=True)
    year_of_passing = models.IntegerField(blank=True)
    division = models.CharField(max_length=1, choices=DIVISION, blank=True)
    percentage = models.FloatField(blank=True)
    medium = models.CharField(max_length=1, choices=MEDIUM, blank=True)

    class Meta:
        db_table = "education_details"
