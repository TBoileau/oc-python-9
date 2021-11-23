import os.path

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client

from litreview import settings
from litreview.models import UserFollows, Ticket, Review


class ReviewsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user+1", "user+1@email.com", "password")
        user = User.objects.create_user("user+2", "user+2@email.com", "password")
        Ticket.objects.create(title="Title", description="description", user=user).save()
        ticket = Ticket.objects.create(title="Title", description="description", user=user)
        ticket.save()
        review = Review.objects.create(ticket=ticket, rating=1, user=user)
        review.save()

    def test_unlogged_user_create_review_should_redirect_to_sign_in(self):
        client = Client()
        response = client.get("/reviews/create/1")
        assert 302 == response.status_code

    def test_create_review_of_ticket_has_already_reviews_should_raise_an_error(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/reviews/create/2")
        assert 400 == response.status_code

    def test_create_review_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/reviews/create/1")
        assert 200 == response.status_code
        response = client.post("/reviews/create/1", {"headline": "headline", "body": "body", "rating": "1"})
        assert 302 == response.status_code
        assert 2 == Review.objects.all().count()

    def test_create_review_without_ticket_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/reviews/create")
        assert 200 == response.status_code
        with open(os.path.join(settings.BASE_DIR, "litreview/static/test.png"), "rb") as image:
            response = client.post(
                "/reviews/create",
                {
                    "headline": "headline",
                    "body": "body",
                    "rating": "1",
                    "title": "Title",
                    "description": "Description",
                    "image": image,
                },
            )
            assert 302 == response.status_code
            assert 2 == Review.objects.all().count()


class TicketsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("user+1", "user+1@email.com", "password")
        User.objects.create_user("user+2", "user+2@email.com", "password")
        Ticket.objects.create(title="Title", description="description", user=user).save()

    def test_unlogged_user_create_ticket_should_redirect_to_sign_in(self):
        client = Client()
        response = client.get("/tickets/create")
        assert 302 == response.status_code

    def test_create_ticket_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/tickets/create")
        assert 200 == response.status_code
        with open(os.path.join(settings.BASE_DIR, "litreview/static/test.png"), "rb") as image:
            response = client.post("/tickets/create", {"title": "Title", "description": "Description", "image": image})
            assert 302 == response.status_code
            assert 2 == Ticket.objects.all().count()

    def test_create_ticket_with_empty_title_should_raise_a_form_error(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/tickets/create")
        assert 200 == response.status_code
        with open(os.path.join(settings.BASE_DIR, "litreview/static/test.png"), "rb") as image:
            response = client.post("/tickets/create", {"title": "", "description": "Description", "image": image})
            assert 200 == response.status_code

    def test_unlogged_user_update_ticket_should_redirect_to_sign_in(self):
        client = Client()
        response = client.get("/tickets/update/1")
        assert 302 == response.status_code

    def test_update_ticket_when_author_is_not_logged_user_should_raise_access_denied(self):
        client = Client()
        client.post("/sign-in", {"username": "user+2", "password": "password"})
        response = client.get("/tickets/update/1")
        assert 403 == response.status_code

    def test_update_ticket_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/tickets/update/1")
        assert 200 == response.status_code
        assert 1 == Ticket.objects.all().count()
        with open(os.path.join(settings.BASE_DIR, "litreview/static/test.png"), "rb") as image:
            response = client.post(
                "/tickets/update/1", {"title": "Title", "description": "Description", "image": image}
            )
            assert 302 == response.status_code
            assert 1 == Ticket.objects.all().count()

    def test_unlogged_user_delete_ticket_should_redirect_to_sign_in(self):
        client = Client()
        response = client.get("/tickets/delete/1")
        assert 302 == response.status_code

    def test_delete_ticket_when_author_is_not_logged_user_should_raise_access_denied(self):
        client = Client()
        client.post("/sign-in", {"username": "user+2", "password": "password"})
        response = client.get("/tickets/delete/1")
        assert 403 == response.status_code

    def test_delete_ticket_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/tickets/delete/1")
        assert 302 == response.status_code
        assert 0 == Ticket.objects.all().count()


class SubscriptionsTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user("user+1", "user+1@email.com", "password")
        user2 = User.objects.create_user("user+2", "user+2@email.com", "password")
        user3 = User.objects.create_user("user+3", "user+3@email.com", "password")
        User.objects.create_user("user+4", "user+3@email.com", "password")
        UserFollows.objects.create(user=user1, followed_user=user2)
        UserFollows.objects.create(user=user2, followed_user=user3)
        UserFollows.objects.create(user=user3, followed_user=user1)

    def test_non_logged_user_should_be_show_his_subscriptions(self):
        client = Client()
        response = client.get("/subscriptions")
        assert 302 == response.status_code

    def test_logged_user_should_be_show_his_subscriptions(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/subscriptions")
        assert 200 == response.status_code

    def test_subscribe_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.post("/subscriptions", {"username": "user+4"})
        assert 302 == response.status_code

    def test_subscribe_non_existing_user_should_be_raise_form_error(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.post("/subscriptions", {"username": "user+fail"})
        assert 200 == response.status_code

    def test_subscribe_user_already_follow_should_be_raise_form_error(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.post("/subscriptions", {"username": "user+2"})
        assert 200 == response.status_code

    def test_unsubscribe_should_be_successful(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        response = client.get("/unsubscribe/2")
        assert 302 == response.status_code
        assert 0 == UserFollows.objects.filter(user_id=1).count()

    def test_unsubscribe_non_existing_user_should_be_raise_an_error(self):
        client = Client()
        client.post("/sign-in", {"username": "user+1", "password": "password"})
        with self.assertRaises(ObjectDoesNotExist):
            client.get("/unsubscribe/20")


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
