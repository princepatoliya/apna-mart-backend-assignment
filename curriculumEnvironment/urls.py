from django.urls import path, include
from curriculumEnvironment.views import SubjectView, SubjectExamView, StudentPerformanceView

urlpatterns = [
  path('subjects/', SubjectView.as_view(), name='subjects'),
  path('subject-exam/', SubjectExamView.as_view(), name="subject-exam"),
  path('performance/', StudentPerformanceView.as_view(), name="subject-exam"),
]
