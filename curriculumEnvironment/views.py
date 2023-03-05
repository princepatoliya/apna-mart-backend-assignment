from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from curriculumEnvironment.serializers import SubjectSerializer, SubjectExamSerializer
from curriculumEnvironment.models import Subject, SubjectExam
from BaseManager.baseRenderers import BaseJsonRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings

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

class SubjectExamView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated, IsAdminUser]

  def post(self, request, format=None):
    subjectExamData = request.data.get("subjectExamData")
    updatedSubjectExamData = list(map(lambda obj: { **obj, 'student_id': request.user.id }, subjectExamData))

    subjectExamSerializer = SubjectExamSerializer(data = updatedSubjectExamData, many=True)
    subjectExamSerializer.is_valid(raise_exception=True)
    subjectExamSerializer.save()

    return Response(subjectExamSerializer.data, status=status.HTTP_201_CREATED)

  def getAllSubjectExam():
    return SubjectExam.objects.all()

class StudentPerformanceView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    subjectExamDataList = SubjectExamView.getAllSubjectExam()

    lowest_exam_score = highest_exam_score = subjectExamDataList[0]
    total_marks = 0
    high_score_board = {}
    highest_score_subject_board = []
    for subjectExam in subjectExamDataList:

      subjectExam.subject_name = subjectExam.subject_id.name

      if subjectExam.marks < lowest_exam_score.marks:
          lowest_exam_score = subjectExam
      
      if subjectExam.marks > highest_exam_score.marks:
          highest_exam_score = subjectExam
          
      total_marks += subjectExam.marks

      if subjectExam.subject_id.id not in high_score_board or subjectExam.marks > high_score_board[subjectExam.subject_id.id].marks:
        high_score_board[subjectExam.subject_id.id] = subjectExam

    total_percentage = round(total_marks * (100 / ( len(subjectExamDataList) * settings.TOTAL_MARK_OF_SUBJECT_EXAM)), 2)
    
    return Response({
      "Overall Percentage" : {
        "value": total_percentage,
        "type": "percentage"
      },
      "Lowest Exam Score" : SubjectExamSerializer(lowest_exam_score).data,
      "Highest Exam Score" : SubjectExamSerializer(highest_exam_score).data,
      "Highest Exam Score Board": SubjectExamSerializer(list(high_score_board.values()), many = True).data
      }, status=status.HTTP_200_OK)