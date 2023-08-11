from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .abstracttable import AbstractTable
from .all_questions import AllQuestions
from app.utility.question_module_functions import validate_check_null


class ExcelQuestions(AbstractTable):
    question_id = models.ForeignKey(AllQuestions, on_delete=models.CASCADE, validators=[validate_check_null])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, validators=[validate_check_null])
    sheet_id = models.CharField(max_length=1000, validators=[validate_check_null])
    question_title = models.CharField(max_length=200, validators=[validate_check_null], unique=True)
    description = models.CharField(max_length=500, validators=[validate_check_null])
    screenshot = models.ImageField(upload_to='excel_screenshots/', blank=True)
    excel_last_edited = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50,default="Excel", validators=[validate_check_null])
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "excel_questions"

    def __str__(self):
        return self.question_title
