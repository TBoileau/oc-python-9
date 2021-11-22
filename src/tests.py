from django.contrib.auth.models import User
from django.test import TestCase, Client



class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('user', 'user@email.com', 'password')

    def test_sign_in_should_be_successful(self):
        client = Client()
        response = client.get('/login')
        assert 200 == response.status_code
        response = client.post('/login', {'username': 'user', 'password': 'password'})
        assert 302 == response.status_code

    def test_sign_in_should_be_raise_an_error_with_wrong_password(self):
        client = Client()
        response = client.get('/login')
        assert 200 == response.status_code
        response = client.post('/login', {'username': 'user', 'password': 'fail'})
        assert 200 == response.status_code

    def test_sign_in_should_be_raise_an_error_with_non_existing_username(self):
        client = Client()
        response = client.get('/login')
        assert 200 == response.status_code
        response = client.post('/login', {'username': 'fail', 'password': 'password'})
        assert 200 == response.status_code
