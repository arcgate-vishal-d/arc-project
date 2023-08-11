from django.db import models

from .abstracttable import AbstractTable
from .paper_setup_description import PaperSetupDescription
from .paper_setup_subject_map import PaperSetupSubjectMap
from .all_questions import AllQuestions


class SubjectQuestionMap(AbstractTable):
    paper_setup_id = models.ForeignKey(PaperSetupDescription, on_delete=models.CASCADE)
    paper_setup_subject_id = models.ForeignKey(PaperSetupSubjectMap, on_delete=models.CASCADE)
    all_question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE)

    class Meta:
        db_table = "subject_question_map"

    def __str__(self):
        return f"{self.paper_setup_id} {self.paper_setup_subject_id} {self.all_question_id}"
