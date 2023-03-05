from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from curriculumEnvironment.serializers import SubjectSerializer, SubjectExamSerializer
from curriculumEnvironment.models import Subject
from BaseManager.baseRenderers import BaseJsonRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


class SubjectView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    subjects = self.getAllSubjects();
    subjectSerializer = SubjectSerializer(subjects, many=True)
    return Response(subjectSerializer.data, status=status.HTTP_200_OK)

  def getAllSubjects(self):
    return Subject.objects.all()

class SubjectExam(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated, IsAdminUser]

  def post(self, request, format=None):
    subjectExamData = request.data.get("subjectExamData")
    updatedSubjectExamData = list(map(lambda obj: { **obj, 'student_id': request.user.id }, subjectExamData))

    subjectExamSerializer = SubjectExamSerializer(data = updatedSubjectExamData, many=True)
    subjectExamSerializer.is_valid(raise_exception=True)
    subjectExamSerializer.save()

    return Response(subjectExamSerializer.data, status=status.HTTP_201_CREATED)