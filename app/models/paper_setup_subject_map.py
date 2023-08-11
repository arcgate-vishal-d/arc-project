from django.db import models

from .abstracttable import AbstractTable
from .paper_setup_description import PaperSetupDescription
from .subjects import Subjects


class PaperSetupSubjectMap(AbstractTable):
    paper_setup_id = models.ForeignKey(PaperSetupDescription, on_delete= models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    subject_time = models.IntegerField()
    subject_marks =  models.IntegerField()
    subject_order = models.IntegerField()
    subject_questions = models.IntegerField()

    class Meta:
        db_table = "paper_setup_subject_map"

    def __str__(self):
        return f'{self.paper_setup_id} {self.subject}'
