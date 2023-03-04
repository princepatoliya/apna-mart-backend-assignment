from django.urls import path, include
from curriculumEnvironment.views import SubjectView, SubjectExam

urlpatterns = [
  path('subjects/', SubjectView.as_view(), name='subjects'),
  path('subjects/exam/', SubjectExam.as_view(), name="subject-exam")
]
