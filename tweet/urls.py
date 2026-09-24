from django.urls import path

from . import views

urlpatterns = [
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/post/<int:tweet_id>/edit/", views.admin_tweet_edit, name="admin_tweet_edit"),
    path("admin/post/<int:tweet_id>/delete/", views.admin_tweet_delete, name="admin_tweet_delete"),
    path("", views.tweet_list, name="tweet_list"),
    path("create/", views.tweet_create, name="tweet_create"),
    path("saved/", views.bookmarks, name="bookmarks"),
    path("register/", views.register, name="register"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("<int:tweet_id>/", views.tweet_detail, name="tweet_detail"),
    path("<int:tweet_id>/edit/", views.tweet_edit, name="tweet_edit"),
    path("<int:tweet_id>/delete/", views.tweet_delete, name="tweet_delete"),
    path("<int:tweet_id>/like/", views.toggle_like, name="toggle_like"),
    path("<int:tweet_id>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
    path("comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
]
