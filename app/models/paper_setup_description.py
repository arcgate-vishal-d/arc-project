from django.db import models

from .abstracttable import AbstractTable
from .test_levels import TestLevels

DEPARTMENT = (
    ('KPO', "KPO"),
    ("SOFTWARE", "SOFTWARE")
)

class PaperSetupDescription(AbstractTable):
    department = models.CharField(
        choices=DEPARTMENT, default='KPO', max_length=50)
    test_level = models.ForeignKey(TestLevels, on_delete=models.CASCADE)
    paper_description = models.CharField(max_length=1000)
    paper_title = models.CharField(max_length=500, unique=True)
    paper_time = models.IntegerField()
    paper_marks = models.IntegerField()

    class Meta:
        db_table = "paper_setup_description"

    def __str__(self):
        return self.paper_title
