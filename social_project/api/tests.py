from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from post.models import Post



class PostsTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username = 'testuser1')
        user.set_password("secret")
        user.save()
        token = Token.objects.create(user=user)
        post = Post.objects.create(owner=user)
     

    def test_single_user(self):
        """ Ensure a test-database has 1 user.
        """
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


    def test_single_post(self):
        """ Ensure a test-database has 1 post.
        """
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)


    def test_get_list_of_posts(self):
        """ Ensure an api can get a list of posts.
        """
        url = reverse("post-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
    

    def test_get_one_post(self):
        """ Ensure an api can get one post.
        """
        post = Post.objects.first()
        url = post.get_api_url()
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)


    def test_post_post_without_user(self):
        """ Ensure an api cann't create a new post without credentials.
        """
        user = self.client.force_authenticate(user=None)
        data = {"title": "Unauthorized creation"}
        url = reverse("post-list")
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_without_user(self):
        """ Ensure an api cann't update a new post without credentials.
        """
        user = self.client.force_authenticate(user=None)
        post = Post.objects.first()
        url = post.get_api_url()
        data = {"title": "Unauthorized change"}
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_post_with_user(self):
        """ Ensure an api can create a new post with user credentials.
        """
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {"title": "Authorized creation"}
        url = reverse("post-list")
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json()['title'],  "Authorized creation") 
        self.assertEqual(Post.objects.count(), 2)
        

    def test_update_post_with_user(self):
        """ Ensure an api can update a posts with user credentials.
        """
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {"title": "Authorized change"}
        post = Post.objects.first()
        url = post.get_api_url()
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)


    def test_user_ownership(self):
        """ Ensure only owner can update a post.
        """
        user2 = User.objects.create(username='testuser2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        post = Post.objects.first()
        self.assertNotEqual(user2.username, post.owner)
        url = post.get_api_url()
        data = {"title": "Alien"}
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_login_and_update_post(self):
        """ Ensure user can login and update its post.
        """
        data = {'username': 'testuser1', 'password': 'secret'}
        url = reverse("rest_framework:login") 
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user__username='testuser1')
        if token is not None:
            post = Post.objects.first()
            url = post.get_api_url()
            data = {"title": "Changed"}
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            r = self.client.put(url, data)
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertEqual(r.json()['title'],  "Changed")
