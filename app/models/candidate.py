import datetime
from django.db import models

from .abstracttable import AbstractTable
from .test_levels import TestLevels


GENDER_CHOICE = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]


class CandidateDetails(AbstractTable):
    test_level = models.ForeignKey(TestLevels, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    dob = models.DateField()
    mobile_no_1 = models.BigIntegerField()
    mobile_no_2 = models.BigIntegerField(null=True,blank=True)
    present_address = models.CharField(max_length=200)
    permanent_address = models.CharField(max_length=200)
    district_present = models.CharField(max_length=100, default=None)
    district_permanent= models.CharField(max_length=100, default=None)
    status = models.IntegerField(default=0)
    profile_progress = models.CharField(max_length=100, default='Pending')
    sheet_id = models.CharField(max_length=500, null=True, blank=True, default=None)
    timer = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "candidate_details"
