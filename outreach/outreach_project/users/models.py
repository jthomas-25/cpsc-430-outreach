from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

ACCOUNT_TYPE_CHOICES = [
    ('student', 'Student'),
    ('employer', 'Employer'),
    ('admin', 'Admin'),
]

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'),unique=True)
    is_pending = models.BooleanField(default=False)#True)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)#False)
    is_student = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    account_type = models.CharField(max_length=10,choices=ACCOUNT_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
