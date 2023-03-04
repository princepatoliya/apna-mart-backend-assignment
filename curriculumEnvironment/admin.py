from django.contrib import admin
from curriculumEnvironment.models import Subject, SubjectExam
# Register your models here.

class SubjectModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'code', 'updated_at')
  search_fields = ('code',)
  ordering = ('id',)


class SubjectExamModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'student_id', 'subject_id', 'marks')
  search_fields = ('student_id', 'subject_id')
  ordering = ('id', 'marks')
  
admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(SubjectExam, SubjectExamModelAdmin)