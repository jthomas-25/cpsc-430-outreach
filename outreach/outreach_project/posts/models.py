from typing import Any
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=10, default="pending", editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=CASCADE, related_name="posts", editable=False)
    #date_posted = models.DateTimeField(default=timezone.now)
    date_posted = models.DateField(default=datetime.date.today, editable=False)
    job_type = models.CharField(max_length=30, default="none")
    end_date = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/posts/' + str(self.id)
        #return reverse('posts/')
    
    def get_date_str(self, date):
        if date:
            return datetime.date.strftime(date, "%m/%d/%Y")
        return "None"
