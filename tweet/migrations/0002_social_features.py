# Generated for the upgraded social experience.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("tweet", "Profile")
    for user in User.objects.all():
        Profile.objects.get_or_create(user_id=user.id)


class Migration(migrations.Migration):

    dependencies = [
        ("tweet", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweet",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tweets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="tweet",
            name="bookmarks",
            field=models.ManyToManyField(blank=True, related_name="bookmarked_tweets", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="tweet",
            name="likes",
            field=models.ManyToManyField(blank=True, related_name="liked_tweets", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="avatars/")),
                ("bio", models.CharField(blank=True, max_length=160)),
                ("location", models.CharField(blank=True, max_length=80)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RunPython(create_profiles, migrations.RunPython.noop),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.CharField(max_length=280)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "tweet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="tweet.tweet",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tweet_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterModelOptions(
            name="tweet",
            options={"ordering": ["-created_at"]},
        ),
    ]
