from django.contrib.auth.models import User
from django.test import TestCase, Client


class SignInTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user", "user@email.com", "password")

    def test_sign_in_should_be_successful(self):
        client = Client()
        response = client.get("/sign-in")
        assert 200 == response.status_code
        response = client.post("/sign-in", {"username": "user", "password": "password"})
        assert 302 == response.status_code

    def test_sign_in_should_be_raise_an_error_with_wrong_password(self):
        client = Client()
        response = client.get("/sign-in")
        assert 200 == response.status_code
        response = client.post("/sign-in", {"username": "user", "password": "fail"})
        assert 200 == response.status_code

    def test_sign_in_should_be_raise_an_error_with_non_existing_username(self):
        client = Client()
        response = client.get("/sign-in")
        assert 200 == response.status_code
        response = client.post("/sign-in", {"username": "fail", "password": "password"})
        assert 200 == response.status_code


class SignUpTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user+1", "user+1@email.com", "password")

    def test_sign_up_should_be_successful(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up",
            {"username": "user", "password": "password", "confirm_password": "password", "email": "user@email.com"},
        )
        assert 302 == response.status_code
        user = User.objects.get(username="user")
        assert "user" == user.username
        assert user.check_password("password")
        assert "user@email.com" == user.email

    def test_sign_up_should_be_raise_an_error_with_existing_username(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up",
            {"username": "user+1", "password": "password", "confirm_password": "password", "email": "user@email.com"},
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_existing_email(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up",
            {"username": "user", "password": "password", "confirm_password": "password", "email": "user+1@email.com"},
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_empty_username(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up",
            {"username": "", "password": "password", "confirm_password": "password", "email": "user@email.com"},
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_empty_password(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up", {"username": "user", "password": "", "confirm_password": "password", "email": "user@email.com"}
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_empty_email(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up", {"username": "user", "password": "password", "confirm_password": "password", "email": ""}
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_empty_confirm_password(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up", {"username": "user", "password": "password", "confirm_password": "", "email": "user@email.com"}
        )
        assert 200 == response.status_code

    def test_sign_up_should_be_raise_an_error_with_confirm_password_not_match_with_password(self):
        client = Client()
        response = client.get("/sign-up")
        assert 200 == response.status_code
        response = client.post(
            "/sign-up",
            {"username": "user", "password": "password", "confirm_password": "fail", "email": "user@email.com"},
        )
        assert 200 == response.status_code
