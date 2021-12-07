from django.db.models.query import EmptyQuerySet, QuerySet
from django.http import request
from django.test import TestCase

from users.models import CustomUser
from posts.models import Post

class test_user_profile_view(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Base123!',bio='base test user')
        self.student = CustomUser.objects.create_user(email='test@mail.umw.edu',password='Student123!',bio='base student test')
        self.user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/myprofile/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_view_uses_correct_template(self):
        login = self.client.login(email='test@test.com',password='Base123!')
        s = self.client.session
        s.update({'user_id':str(self.user.id)})
        s.save()
        response = self.client.get('/users/myprofile/',follow=True)
        
        self.assertEqual(str(response.context['user']),self.user.email)

        self.assertTemplateUsed(response,'user_profile.html')

class test_user_login_view(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/login/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_view_uses_correct_template(self):
        response = self.client.get('/users/login/',follow=True)
        self.assertTemplateUsed(response,'user_login_form.html')
    def test_view_logs_in(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        self.assertTrue(login)

class test_user_create_view(TestCase):
    @classmethod
    def setUp(self):
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/create/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_view_uses_correct_template(self):
        response = self.client.get('/users/create/',follow=True)
        self.assertTemplateUsed(response,'user_create_form.html')

class test_user_edit_view(TestCase):
    @classmethod
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/edit/'+str(self.user.id),follow=True)
        self.assertEqual(response.status_code,200)
    def test_view_uses_correct_template(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        s = self.client.session
        s.update({'user_id':self.user.id,'is_admin':False})
        s.save()
        response = self.client.get('/users/edit/'+str(self.user.id),follow=True)
        
        self.assertEqual(str(response.context['user']),self.user.email)

        self.assertTemplateUsed(response,'user_change_form.html')

class test_user_logout_view(TestCase):
    @classmethod 
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.user.save()
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/logout/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_logout_destroys_session(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        s = self.client.session
        s.update({'user_id':self.user.id,'is_admin':False})
        s.save()
        response = self.client.get('/users/logout/',follow=True)
        self.assertNotEqual(str(response.context['user']),str(self.user))
class test_user_list_view(TestCase):
    @classmethod 
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.student = CustomUser.objects.create_user(email='test@mail.umw.edu',password='Student123!',bio='base student test')
        self.user.save()
        self.student.save()
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_user_list_has_all_users(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        response = self.client.get('/users/',follow=True)
        users = CustomUser.objects.all()
        for x in users:
            self.assertTrue(x in response.context['users'])

    def test_list_view_uses_correct_template(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        response = self.client.get('/users/',follow=True)
        
        self.assertTemplateUsed(response,'user_list.html')


class test_user_detail_view(TestCase):
    @classmethod 
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.student = CustomUser.objects.create_user(email='test@mail.umw.edu',password='Student123!',bio='base student test')
        self.user.save()
        self.student.save()
    def test_detail_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/view/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_detail_view_uses_correct_template(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        response = self.client.get('/users/view/?user='+str(self.user.id),follow=True)
        
        self.assertTemplateUsed(response,'user_detail.html')


class test_account_delete_view(TestCase):
    @classmethod 
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com',password='Test123!',bio='base user test')
        self.user.save()
    def test_delete_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/myprofile/delete/',follow=True)
        self.assertEqual(response.status_code,200)
    def test_delete_view_deletes_user_and_session(self):
        login = self.client.login(email='test@test.com',password='Test123!')
        s = self.client.session
        s.update({'user_id':self.user.id,'is_admin':False})
        s.save()
        response = self.client.get('/users/myprofile/delete/',follow=True)
        new = self.client.session
        self.assertTrue('user_id' not in new.keys())
        self.assertFalse(self.user in CustomUser.objects.all())

class test_contact_user_view(TestCase):
    @classmethod 
    def setUp(self):
        self.receiver = CustomUser.objects.create_user(email='receiver@test.com',password='Test123!',bio='base user test')
        self.post = Post.objects.create(user_id_id=self.receiver.id,title='Test Post',description='Test Contact')
        self.post.save()
        self.receiver.save()
    def test_contact_user_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/contact/'+str(self.post.id),follow=True)
        self.assertEqual(response.status_code,200)

