from django.db import models
from account.models import User

# Create your models here.

class Subject(models.Model):
  name = models.CharField(max_length=80, unique=True)
  code = models.CharField(max_length=10, unique=True)
  description = models.CharField(max_length=250)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
    
  def __str__(self):
      return f'{self.code} : {self.name}'

class SubjectExam(models.Model):
  class Meta:
    unique_together = (('student_id', 'subject_id'),)

  student_id = models.ForeignKey(User, on_delete=models.CASCADE)
  subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
  marks = models.FloatField()