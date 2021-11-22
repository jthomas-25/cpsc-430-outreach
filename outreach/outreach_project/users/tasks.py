from django.utils import timezone
from .models import CustomUser


"""
To schedule this task:

python3 manage.py shell
from django_q.models import Schedule
Schedule.objects.create(
    func='users.tasks.delete_graduated_students',
    schedule_type=Schedule.YEARLY,
    repeats=-1
)

This task is now scheduled to delete all student accounts after their graduation dates once per year.

To run a scheduled task: python3 manage.py qcluster
"""
def delete_graduated_students():
    print("Checking for accounts to delete...")
    now = timezone.now()
    graduated_students = CustomUser.objects.filter(is_student=True, graduation_date__lte=now)
    if graduated_students:
        print("Deleting accounts...")
        for student in graduated_students:
            print("Deleting " + str(student) + "...")
            student.delete()
            print("Deleted.")
        #graduated_students.delete()
    print("All accounts up to date.")
