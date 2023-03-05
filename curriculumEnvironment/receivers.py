from curriculumEnvironment.models import SubjectExam

@receiver(post_save, sender=SubjectExam)
def calculate_student_result(sender, instance=None, created=False, **kwargs):
  if created:
    print("helloooooooooo")
    print("sender: ", sender)
    print("instance: ", instance)
    print("instance: ", instance.marks)