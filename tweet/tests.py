from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Tweet


class TweetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="strong-pass-123")
        self.tweet = Tweet.objects.create(user=self.user, text_field="Hello from Pulse")

    def test_feed_loads(self):
        response = self.client.get(reverse("tweet_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello from Pulse")

    def test_create_requires_login(self):
        response = self.client.get(reverse("tweet_create"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_like(self):
        self.client.login(username="tester", password="strong-pass-123")
        self.client.post(reverse("toggle_like", args=[self.tweet.id]))
        self.assertTrue(self.tweet.likes.filter(pk=self.user.pk).exists())


class ControlCenterTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="strong-pass-123")
        self.staff = User.objects.create_user(
            username="moderator",
            password="strong-pass-123",
            is_staff=True,
        )
        self.post = Tweet.objects.create(user=self.author, text_field="A post owned by another user")

    def test_control_center_requires_staff(self):
        self.client.login(username="author", password="strong-pass-123")
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_staff_can_open_control_center(self):
        self.client.login(username="moderator", password="strong-pass-123")
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A post owned by another user")

    def test_staff_can_edit_another_users_post(self):
        self.client.login(username="moderator", password="strong-pass-123")
        response = self.client.post(
            reverse("admin_tweet_edit", args=[self.post.id]),
            {"text_field": "Moderated content"},
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text_field, "Moderated content")

    def test_staff_can_delete_another_users_post(self):
        self.client.login(username="moderator", password="strong-pass-123")
        response = self.client.post(reverse("admin_tweet_delete", args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tweet.objects.filter(pk=self.post.id).exists())
