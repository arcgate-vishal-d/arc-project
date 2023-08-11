from django.db import models

from .abstracttable import AbstractTable
from .candidate_result_individual import CandidateResultIndividual
from .grades import Grades


class CandidateResults(AbstractTable):
    candidate = models.ForeignKey(CandidateResultIndividual, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grades, on_delete=models.SET_NULL, null=True)


    class Meta:
        db_table = "candidate_result"
