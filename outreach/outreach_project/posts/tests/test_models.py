from django.test import TestCase

from users.models import CustomUser
from posts.models import Post
import datetime

class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password='TestPass1',
            bio='I am a test user.')
        cls.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.',
            user_id=cls.user)
        cls.user.save()
        cls.post.save()

    # Field tests
    def test_title_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('title').verbose_name
        self.assertEqual(label, "title")

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)
    
    def test_description_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('description').verbose_name
        self.assertEqual(label, "description")

    def test_status_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('status').verbose_name
        self.assertEqual(label, "status")

    def test_status_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('status').max_length
        self.assertEqual(max_length, 10)
        
    def test_status_default_value_is_pending(self):
        post = Post.objects.get(id=1)
        default = post._meta.get_field('status').default
        self.assertEqual(default, "pending")

    def test_status_is_not_editable(self):
        post = Post.objects.get(id=1)
        editable = post._meta.get_field('status').editable
        self.assertFalse(editable)

    def test_user_id_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('user_id').verbose_name
        self.assertEqual(label, "user id")
    
    def test_user_id_is_related_to_customuser_model(self):
        post = Post.objects.get(id=1)
        related_model = post._meta.get_field('user_id').related_model
        self.assertIs(related_model, CustomUser)

    def test_user_id_is_nullable(self):
        post = Post.objects.get(id=1)
        null = post._meta.get_field('user_id').null
        self.assertTrue(null)
    
    def test_user_id_is_not_editable(self):
        post = Post.objects.get(id=1)
        editable = post._meta.get_field('user_id').editable
        self.assertFalse(editable)

    def test_date_posted_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('date_posted').verbose_name
        self.assertEqual(label, "date posted")
    
    def test_date_posted_default_value_is_today(self):
        post = Post.objects.get(id=1)
        default = post._meta.get_field('date_posted').default
        self.assertEqual(default, datetime.date.today)
    
    def test_date_posted_is_not_editable(self):
        post = Post.objects.get(id=1)
        editable = post._meta.get_field('date_posted').editable
        self.assertFalse(editable)
    
    def test_job_type_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('job_type').verbose_name
        self.assertEqual(label, "job type")

    def test_job_type_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('job_type').max_length
        self.assertEqual(max_length, 30)
        
    def test_job_type_default_value_is_none(self):
        post = Post.objects.get(id=1)
        default = post._meta.get_field('job_type').default
        self.assertEqual(default, "none")

    def test_end_date_label(self):
        post = Post.objects.get(id=1)
        label = post._meta.get_field('end_date').verbose_name
        self.assertEqual(label, "end date")
    
    def test_end_date_default_value_is_none(self):
        post = Post.objects.get(id=1)
        default = post._meta.get_field('end_date').default
        self.assertIsNone(default)
        
    def test_end_date_is_nullable(self):
        post = Post.objects.get(id=1)
        null = post._meta.get_field('end_date').null
        self.assertTrue(null)
    
    def test_end_date_is_allowed_to_be_blank(self):
        post = Post.objects.get(id=1)
        blank = post._meta.get_field('end_date').blank
        self.assertTrue(blank)

    # Method tests
    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        blank = post._meta.get_field('end_date').blank
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), '/posts/1')
    
    def test_get_date_str(self):
        post = Post.objects.get(id=1)
        date_posted_str = post.get_date_str(post.date_posted)
        todays_date_str = datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")
        self.assertEqual(date_posted_str, todays_date_str)

