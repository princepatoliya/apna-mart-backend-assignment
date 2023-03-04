from rest_framework import serializers
from curriculumEnvironment.models import Subject, SubjectExam
from django.conf import settings

class SubjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subject
    fields = ('id', 'name', 'code', 'description')

class SubjectExamSerializer(serializers.ModelSerializer):

  class Meta:
    model = SubjectExam
    fields = ('student_id', 'subject_id', 'marks')
    extra_kwargs= {
      'student_id': { 'required': False, 'write_only': True },
    }