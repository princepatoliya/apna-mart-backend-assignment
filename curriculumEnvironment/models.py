from django.db import models
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Subject(models.Model):
  name = models.CharField(max_length=80, unique=True)
  code = models.CharField(max_length=10, unique=True)
  description = models.CharField(max_length=250)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
    
  def __str__(self):
      return f'{self.name}'

class SubjectExam(models.Model):
  student_id = models.ForeignKey(User, on_delete=models.CASCADE)
  subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
  marks = models.FloatField()
  exam_type = models.CharField(max_length=20, default="Test")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

# class OverallStudentScore(models.Model):
#   student_id = models.ForeignKey(User, on_delete=models.CASCADE)
#   overall_score = models.FloatField(default=0)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

# class highestSubjectExamScore(models.Model):
#   student_id = models.ForeignKey(User, on_delete=models.CASCADE)
#   subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
#   highest_subject_exam = models.ForeignKey(SubjectExam, on_delete=models.CASCADE)
#   lowest_subject_exam = models.ForeignKey(SubjectExam, on_delete=models.CASCADE)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)