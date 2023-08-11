import datetime
from django.db import models

from .abstracttable import AbstractTable
from .candidate import CandidateDetails


SOURCE = [
    ('CAMPUS', 'Arcgate Campus Drive'),
    ('WEBSITE', 'Arcgate Website'),
    ('EMPLOYEE', 'Arcgate Employee Referral'),
    ('FRIENDS', 'Friends/Family'),
    ('NEWSPAPER', 'Newspaper'),
    ('SOCIAL MEDIA', 'Arcgate Social Media'),
    ('WALK IN', 'Walk-In'),
    ('CONSULTANCY', 'Job Consultancy'),
    ('OTHER', 'Others'),

]
NEWSPAPER = [
    ('PATRIKA', 'Rajasthan Patrika'),
    ('BHASKAR', 'Dainik Bhaskar'),
    ('OTHER', 'Other')
]


class CandidateSourceOfInformation(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    previous_interviewed = models.BooleanField(default=False)
    previous_worked = models.BooleanField(default=False)
    source_of_info = models.CharField(max_length=500, choices=SOURCE)
    newspaper = models.CharField(choices=NEWSPAPER, max_length=100, blank=True)
    consultancy = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "source_of_information"
