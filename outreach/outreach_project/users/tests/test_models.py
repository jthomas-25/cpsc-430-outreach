from django.db import models
from django.test import TestCase

from users.models import CustomUser

class UserModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('setUpTestData')
        baseUser = CustomUser.objects.create(email='bennm23@gmail.com',bio='Test Bio')
        studentUser = CustomUser.objects.create(email='user@mail.umw.edu',graduation_date= '2022-01-01' )
        pass
    
    def setUp(self):
        print('setUp')
        pass
    def test_email_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('email').verbose_name
        self.assertEqual(label,'email address')
    def test_object_name_is_email(self):
        base = CustomUser.objects.get(id = 1)
        expected = base.email
        self.assertEqual(str(base),expected)
        
    def test_pending_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_pending').verbose_name
        self.assertEqual(label,'is pending')
    def test_active_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_active').verbose_name
        self.assertEqual(label,'is active')
    def test_blocked_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_blocked').verbose_name
        self.assertEqual(label,'is blocked')   
    def test_admin_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_admin').verbose_name
        self.assertEqual(label,'is admin')
    def test_student_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_student').verbose_name
        self.assertEqual(label,'is student')
    def test_employer_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_employer').verbose_name
        self.assertEqual(label,'is employer')   
    def test_staff_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('is_staff').verbose_name
        self.assertEqual(label,'is staff')
    def test_date_joined_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('date_joined').verbose_name
        self.assertEqual(label,'date joined')
    def test_graduation_date_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('graduation_date').verbose_name
        self.assertEqual(label,'graduation date')
    def test_bio_label(self):
        base = CustomUser.objects.get(id = 1)
        label = base._meta.get_field('bio').verbose_name
        self.assertEqual(label,'bio')