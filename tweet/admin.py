from django.contrib import admin

from .models import Comment, Profile, Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_text", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("text_field", "user__username")
    ordering = ("-created_at",)

    @admin.display(description="Post")
    def short_text(self, obj):
        return obj.text_field[:60]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tweet", "created_at")
    search_fields = ("body", "user__username", "tweet__text_field")
    ordering = ("-created_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location")
    search_fields = ("user__username", "user__email", "bio", "location")
