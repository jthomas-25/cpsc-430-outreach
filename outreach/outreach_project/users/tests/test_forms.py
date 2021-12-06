from datetime import date
from django import forms
from django.forms.forms import BaseForm
from django.test import TestCase

from users.forms import CustomUserCreationForm,CustomUserChangeForm

class Test_Custom_User_Creation_Form(TestCase):
    def test_all_fields_present(self):
        form = CustomUserCreationForm()
        fields = ('email','graduation_date','bio')
        self.assertTrue(fields,form.fields.keys)
    def test_graduation_date_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(
            form.fields['graduation_date'].label =='graduation date' 
            or 
            form.fields['graduation_date'].label is None
        )
    def test_graduation_date_field_date_widget(self):
        form = CustomUserCreationForm()
        year_label = ('','Choose Year')
        month_label = ('','Choose Month')
        day_label = ('','Choose Day')
        self.assertTrue(
            form._meta.widgets['graduation_date'].day_none_value == day_label
            and 
            form._meta.widgets['graduation_date'].month_none_value == month_label
            and
            form._meta.widgets['graduation_date'].year_none_value == year_label
        )
    def test_bio_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(
            form.fields['bio'].label == 'Bio'
            or
            form.fields['bio'].label == None
        )
    def test_bio_field_placeholder_value(self):
        form = CustomUserCreationForm()
        expected = 'Enter a bio'
        self.assertEqual(form._meta.widgets['bio'].attrs['placeholder'],expected)
    def test_email_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(
            form.fields['email'].label == 'Email address'
            or
            form.fields['email'].label == None
        )
    def test_email_field_placeholder_value(self):
        form = CustomUserCreationForm()
        expected = 'Email'
        self.assertEqual(form._meta.widgets['email'].attrs['placeholder'],expected)


class Test_Custom_User_Change_Form(TestCase):
    def setUp(self):
        self.baseForm = CustomUserChangeForm(None,is_student = False)
        self.studentForm = CustomUserChangeForm(None,is_student= True)
    def test_all_fields_present_for_student(self):
        fields = ('email','graduation_date','bio')
        self.assertTrue(fields,self.baseForm.fields.keys)
    def test_all_fields_present_for_not_student(self):
        fields = ('email','bio')
        self.assertTrue(fields,self.studentForm.fields.keys)
    def test_password_not_included(self):
        keys = self.baseForm.fields.keys()
        self.assertFalse('password' in keys)
    def test_graduation_date_field_label_in_student_form(self):
        self.assertTrue(
            self.studentForm.fields['graduation_date'].label =='Graduation date' 
            or 
            self.studentForm.fields['graduation_date'].label is None
        )
    def test_graduation_date_field_date_widget_student_form(self):
        year_label = ('','Choose Year')
        month_label = ('','Choose Month')
        day_label = ('','Choose Day')
        self.assertTrue(
            self.studentForm._meta.widgets['graduation_date'].day_none_value == day_label
            and 
            self.studentForm._meta.widgets['graduation_date'].month_none_value == month_label
            and
            self.studentForm._meta.widgets['graduation_date'].year_none_value == year_label
        )
    def test_bio_field_label(self):
        form = self.baseForm
        self.assertTrue(
            form.fields['bio'].label == 'Bio'
            or
            form.fields['bio'].label == None
        )
    def test_email_field_label(self):
        form = self.baseForm
        self.assertTrue(
            form.fields['email'].label == 'Email address'
            or
            form.fields['email'].label == None
        )

   