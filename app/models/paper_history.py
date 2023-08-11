from django.db import models

from .abstracttable import AbstractTable
from .paper_setup_description import PaperSetupDescription
from django.contrib.auth.models import User


class PaperHistory(AbstractTable):
    paper_set = models.ForeignKey(
        PaperSetupDescription, on_delete=models.CASCADE)
    set_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        db_table = "paper_history"
