from django.db import models

from .abstracttable import AbstractTable
from .education_details import CandidateDetails
from .paper_setup_description import PaperSetupDescription
from .paper_setup_subject_map import PaperSetupSubjectMap
from .subject_question_map import SubjectQuestionMap


ANSWER_STATUS = [
    ('Correct', 'Correct'),
    ('Incorrect', 'Incorrect'),
]


class CandidateResultIndividual(AbstractTable):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    paper_set_id = models.ForeignKey(PaperSetupDescription, on_delete=models.SET_NULL, null=True)
    subject_question_id = models.ForeignKey(SubjectQuestionMap, on_delete=models.SET_NULL, null=True)
    paper_subject_id = models.ForeignKey(PaperSetupSubjectMap,on_delete=models.SET_NULL, null=True )
    answer_marks = models.FloatField()
    candidate_answer = models.CharField(max_length=500, blank=True)
    answer_status = models.CharField(max_length=24, choices=ANSWER_STATUS, default="Incorrect")

    class Meta:
        db_table = "candidate_result_individual"
