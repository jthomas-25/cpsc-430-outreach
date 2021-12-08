from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from posts.models import Post

# Unhashed password for login
PASSWORD = 'TestPass1'

class HomeViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        for i in range(5):
            post = Post.objects.create(
                title='Test Post' + str(i),
                description='This is a test post.',
                status='active')
            post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id) }
        session.update(user_id)
        session.save()

    def test_view_gets_correct_url(self):
        url = reverse('home:index')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = reverse('home:index')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('home_view.html')

    def test_all_active_posts_listed(self):
        self.login(self.client)
        url = reverse('posts:list')
        response = self.client.get(url, follow=True)
        posts = Post.objects.filter(status="active")
        for post in posts:
            self.assertTrue(post in response.context['post_list'])

class AdminPortalViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
    
    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()

    def test_view_gets_correct_url(self):
        url = reverse('home:admin-portal')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = reverse('home:admin-portal')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('admin_portal_view.html')
