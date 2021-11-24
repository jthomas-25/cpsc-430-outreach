from django.utils import timezone
from .models import Post

#To run a scheduled task: python3 manage.py qcluster

#Working on deleting posts at the end of the semester.

"""
To schedule this task:

python3 manage.py shell
from django_q.models import Schedule
Schedule.objects.create(
    func='posts.tasks.delete_expired_posts',
    schedule_type=Schedule.DAILY,
    repeats=-1
)

Runs once per day.
"""
def delete_expired_posts():
    print("Checking for expired posts...")
    now = timezone.now()
    expired_posts = Post.objects.filter(end_date__isnull=False, end_date__lt=now)
    if expired_posts:
        print("Deleting posts...")
        #expired_posts.delete()
        for post in expired_posts:
            #print("Title: " + post.title + ", End date: " + str(post.end_date))
            print("Deleting " + str(post) + "...")
            post.delete()
            print("Deleted.")
    print("All posts up to date.")

"""
To schedule this task:

python3 manage.py shell
from django_q.models import Schedule
Schedule.objects.create(
    func='posts.tasks.delete_posts_with_no_end_date',
    schedule_type=Schedule.QUARTERLY,
    repeats=-1
)

Runs every 3 months.
"""
def delete_posts_with_no_end_date():
    print("Checking for posts with no end date...")
    posts = Post.objects.filter(end_date__isnull=True)
    if posts:
        print("Deleting posts...")
        #posts.delete()
        for post in posts:
            print("Deleting " + str(post) + "...")
            post.delete()
            print("Deleted.")
    print("All posts up to date.")
