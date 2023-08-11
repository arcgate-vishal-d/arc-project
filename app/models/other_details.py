import datetime
from django.db import models

from .abstracttable import AbstractTable
from .candidate import CandidateDetails


SHIFT = [
    ('D', 'Day'),
    ('N', 'Night'),
    ('A', 'Any')
]


class CandidateOtherDetails(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    service_commitment = models.BooleanField()
    salary_security = models.BooleanField()
    shift = models.CharField(max_length=1, choices=SHIFT)
    expected_joining_date = models.DateField()
    salary_expected = models.FloatField(blank=True)

    class Meta:
        db_table = "other_details"
