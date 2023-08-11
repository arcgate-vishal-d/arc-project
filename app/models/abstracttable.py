from django.db import models
from django.utils import timezone


class AbstractTable(models.Model):
    created = models.DateTimeField(default=timezone.localtime())
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
