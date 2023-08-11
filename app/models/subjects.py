from django.db import models
from django.contrib.auth.models import User
from app.models.abstracttable import AbstractTable

class Subjects(AbstractTable):
    subject = models.CharField(max_length=100,unique= True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        db_table = 'subject'
