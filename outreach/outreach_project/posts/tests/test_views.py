from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from posts.models import Post

# Unhashed password for login
PASSWORD = 'TestPass1'

class PostListViewTestCase(TestCase):
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
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()

    def test_view_gets_correct_url(self):
        url = reverse('posts:list')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = reverse('posts:list')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_list.html')

    def test_all_active_posts_listed(self):
        self.login(self.client)
        url = reverse('posts:list')
        response = self.client.get(url, follow=True)
        posts = Post.objects.filter(status="active")
        for post in posts:
            self.assertTrue(post in response.context['post_list'])


class PostCreateViewTestCase(TestCase):
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
        url = reverse('posts:create')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = reverse('posts:create')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_create_form.html')

class PostEditViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.')
        self.post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()
    
    def test_view_gets_correct_url(self):
        url = '/posts/edit/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = '/posts/edit/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_edit_form.html')

class PostDeleteViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.')
        self.post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()
    
    def test_view_gets_correct_url(self):
        url = '/posts/delete/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = '/posts/delete/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_confirm_delete.html')

class SearchPostsViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.')
        self.post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()
    
    def test_view_gets_correct_url(self):
        url = '/posts/search'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = '/posts/search'
        response = self.client.get(url)
        self.assertTemplateUsed('search2.html')

class MyPostsViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.')
        self.post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()
    
    def test_view_gets_correct_url(self):
        url = reverse('posts:mine')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = reverse('posts:mine')
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_mine.html')

class PostDetailViewTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            password=PASSWORD,
            bio='I am a test user.')
        self.user.save()
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post.')
        self.post.save()

    @classmethod
    def login(self, client):
        client.login(email=self.user.email,password=PASSWORD)
        session = client.session
        user_id = {'user_id': str(self.user.id)}
        session.update(user_id)
        session.save()

    def test_view_gets_correct_url(self):
        url = '/posts/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_gets_correct_template(self):
        self.login(self.client)
        url = '/posts/' + str(self.post.id)
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed('post_detail.html')
