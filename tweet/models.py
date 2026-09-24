from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    text_field = models.TextField(max_length=240)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="liked_tweets", blank=True)
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_tweets", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.text_field[:40]}"


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweet_comments")
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} on Tweet #{self.tweet_id}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
