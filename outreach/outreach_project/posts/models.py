from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=10, default="pending", editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts/')
