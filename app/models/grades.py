from django.db import models
from django.core.exceptions import ValidationError

from .abstracttable import AbstractTable


class Grades(AbstractTable):
    title = models.CharField(max_length=100,unique= True)
    grade_from = models.DecimalField(max_digits=4, decimal_places=2)
    grade_to = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "grades"

    def __str__(self):
        return self.title
