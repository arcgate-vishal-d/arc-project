from django.db import models

from .abstracttable import AbstractTable
from django.contrib.auth.models import User


class TestLevels(AbstractTable):
    test_level = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_level

    class Meta:
        db_table = 'test_levels'

    def __str__(self):
        return self.test_level
