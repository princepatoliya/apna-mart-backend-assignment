from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from curriculumEnvironment.serializers import SubjectSerializer, SubjectExamSerializer
from curriculumEnvironment.models import Subject, SubjectExam
from BaseManager.baseRenderers import BaseJsonRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# constant
GET_ALL_SUBJECTS = "get-all-subjects"
GET_SUBJECT_EXAM = "get-subject-exam"
GET_STUDENT_PERFORMANCE = "get-student-performance"

# Create your views here.

class SubjectView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated]


  def get(self, request, format=None):
    subjects = SubjectView.getAllSubjects();
    subjectSerializer = SubjectSerializer(subjects, many=True)
    return Response(subjectSerializer.data, status=status.HTTP_200_OK)

  def getAllSubjects():
    if cache.get(GET_ALL_SUBJECTS):
      print("subject from cache....")
      return cache.get(GET_ALL_SUBJECTS)

    subjectList = Subject.objects.all()
    cache.set(GET_ALL_SUBJECTS, subjectList, settings.CACHE_TTL)
    print("subject from DB....")
    return subjectList

class SubjectExamView(APIView):
  renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated, IsAdminUser]


  def post(self, request, format=None):
    subjectExamData = request.data.get("subjectExamData")
    subjectExamSerializer = SubjectExamSerializer(data = subjectExamData, many=True)
    subjectExamSerializer.is_valid(raise_exception=True)
    subjectExamSerializer.save()

    return Response(subjectExamSerializer.data, status=status.HTTP_201_CREATED)

  def getAllSubjectExamByStudentId(studentId):
    if cache.get(f'{GET_SUBJECT_EXAM}-{studentId}'):
      print("examData from cache....")
      return cache.get(f'{GET_SUBJECT_EXAM}-{studentId}')
    
    studentExamData = SubjectExam.objects.filter(student_id=studentId);
    cache.set(f'{GET_SUBJECT_EXAM}-{studentId}', studentExamData, settings.CACHE_TTL)
    print("examData from DB....")
    return SubjectExam.objects.filter(student_id=studentId)

class StudentPerformanceView(APIView):
  # renderer_classes = [BaseJsonRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    if cache.get(f'{GET_STUDENT_PERFORMANCE}-{request.user.id}'):
      print("performance data from cache....")
      return Response(cache.get(f'{GET_STUDENT_PERFORMANCE}-{request.user.id}'), status=status.HTTP_200_OK)
    
    subjectExamDataList = SubjectExamView.getAllSubjectExamByStudentId(request.user.id)
    if not subjectExamDataList:
      return Response({}, status=status.HTTP_201_CREATED)

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
    
    response_data = {
      "Overall Percentage" : {
        "value": total_percentage,
        "type": "percentage"
      },
      "Lowest Exam Score" : SubjectExamSerializer(lowest_exam_score).data,
      "Highest Exam Score" : SubjectExamSerializer(highest_exam_score).data,
      "Highest Exam Score Board": SubjectExamSerializer(list(high_score_board.values()), many = True).data
    }
    print("performance data from DB....")
    cache.set(f'{GET_STUDENT_PERFORMANCE}-{request.user.id}', response_data, settings.CACHE_TTL)

    return Response(response_data, status=status.HTTP_200_OK)