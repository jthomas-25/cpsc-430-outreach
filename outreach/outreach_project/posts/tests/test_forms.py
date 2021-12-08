from django.test import TestCase

from posts.forms import job_types, PostCreateForm, PostEditForm

class PostCreateFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = PostCreateForm()
    
    # Field tests
    def test_all_fields_available(self):
        fields = ['title', 'description', 'job_type', 'end_date']
        self.assertEqual(fields, list(self.form.fields.keys()))
    
    def test_title_field_label(self):
        self.assertTrue(
            self.form.fields['title'].label is None
            or
            self.form.fields['title'].label == 'Title'
        )
    
    def test_description_field_label(self):
        self.assertTrue(
            self.form.fields['description'].label is None
            or
            self.form.fields['description'].label == 'Description'
        )

    def test_job_type_field_label(self):
        self.assertTrue(
            self.form.fields['job_type'].label is None
            or
            self.form.fields['job_type'].label == 'Job type'
        )

    def test_job_type_field_select_widget(self):
        choices = self.form._meta.widgets['job_type'].choices
        self.assertEqual(choices, job_types)
    
    def test_end_date_field_label(self):
        self.assertTrue(
            self.form.fields['end_date'].label is None
            or
            self.form.fields['end_date'].label == 'End date'
        )

    def test_end_date_field_label_select_date_widget(self):
        month_choice = self.form._meta.widgets['end_date'].month_none_value
        day_choice = self.form._meta.widgets['end_date'].day_none_value
        year_choice = self.form._meta.widgets['end_date'].year_none_value
        month_label = ('', 'Month')
        day_label = ('', 'Day')
        year_label = ('', 'Year')
        choices = [month_choice, day_choice, year_choice]
        labels = [month_label, day_label, year_label]
        self.assertEqual(choices, labels)    

class PostEditFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = PostEditForm()
    
    # Field tests
    def test_all_fields_available(self):
        fields = ['title', 'description', 'job_type', 'end_date']
        self.assertEqual(fields, list(self.form.fields.keys()))
    
    def test_title_field_label(self):
        self.assertTrue(
            self.form.fields['title'].label is None
            or
            self.form.fields['title'].label == 'Title'
        )
    
    def test_description_field_label(self):
        self.assertTrue(
            self.form.fields['description'].label is None
            or
            self.form.fields['description'].label == 'Description'
        )

    def test_job_type_field_label(self):
        self.assertTrue(
            self.form.fields['job_type'].label is None
            or
            self.form.fields['job_type'].label == 'Job type'
        )
    
    def test_job_type_field_select_widget(self):
        choices = self.form._meta.widgets['job_type'].choices
        self.assertEqual(choices, job_types)
    
    def test_end_date_field_label(self):
        self.assertTrue(
            self.form.fields['end_date'].label is None
            or
            self.form.fields['end_date'].label == 'End date'
        )
    
    def test_end_date_field_label_select_date_widget(self):
        month_choice = self.form._meta.widgets['end_date'].month_none_value
        day_choice = self.form._meta.widgets['end_date'].day_none_value
        year_choice = self.form._meta.widgets['end_date'].year_none_value
        month_label = ('', 'Month')
        day_label = ('', 'Day')
        year_label = ('', 'Year')
        choices = [month_choice, day_choice, year_choice]
        labels = [month_label, day_label, year_label]
        self.assertEqual(choices, labels)

