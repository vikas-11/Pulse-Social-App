from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import (
    CommentForm,
    ProfileForm,
    TweetForm,
    UserRegistrationForm,
    UserUpdateForm,
)
from .models import Comment, Profile, Tweet



def _staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_active and user.is_staff,
        login_url="login",
    )(view_func)

def _safe_next(request, fallback):
    target = request.POST.get("next")
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        return target
    return reverse(fallback)


def _tweet_queryset():
    return (
        Tweet.objects.select_related("user")
        .prefetch_related("likes", "bookmarks")
        .annotate(like_count=Count("likes", distinct=True), comment_count=Count("comments", distinct=True))
    )


def tweet_list(request):
    query = request.GET.get("q", "").strip()
    tweets = _tweet_queryset()

    if query:
        tweets = tweets.filter(
            Q(text_field__icontains=query)
            | Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(tweets, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "tweets": page_obj,
        "page_obj": page_obj,
        "query": query,
        "total_tweets": Tweet.objects.count(),
        "total_people": User.objects.count(),
    }
    return render(request, "tweet/tweet_list.html", context)


def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(_tweet_queryset(), pk=tweet_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please sign in to join the conversation.")
            return redirect(f"{reverse('login')}?next={request.path}")

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.tweet = tweet
            comment.user = request.user
            comment.save()
            messages.success(request, "Your reply was posted.")
            return redirect("tweet_detail", tweet_id=tweet.id)
    else:
        comment_form = CommentForm()

    comments = tweet.comments.select_related("user").all()
    return render(
        request,
        "tweet/tweet_detail.html",
        {"tweet": tweet, "comments": comments, "comment_form": comment_form},
    )


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Your post is live.")
            return redirect("tweet_detail", tweet_id=tweet.id)
    else:
        form = TweetForm()

    return render(request, "tweet/tweet_form.html", {"form": form, "mode": "create"})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("tweet_detail", tweet_id=tweet.id)
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweet/tweet_form.html", {"form": form, "mode": "edit", "tweet": tweet})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        tweet.delete()
        messages.success(request, "Post deleted.")
        return redirect("tweet_list")

    return render(request, "tweet/tweet_confirm_delete.html", {"tweet": tweet})


@login_required
@require_POST
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.likes.filter(pk=request.user.pk).exists():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    return redirect(_safe_next(request, "tweet_list"))


@login_required
@require_POST
def toggle_bookmark(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.bookmarks.filter(pk=request.user.pk).exists():
        tweet.bookmarks.remove(request.user)
        messages.info(request, "Removed from saved posts.")
    else:
        tweet.bookmarks.add(request.user)
        messages.success(request, "Saved for later.")
    return redirect(_safe_next(request, "tweet_list"))


@login_required
def bookmarks(request):
    tweets = _tweet_queryset().filter(bookmarks=request.user)
    paginator = Paginator(tweets, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "tweet/bookmarks.html", {"tweets": page_obj, "page_obj": page_obj})


@login_required
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if not request.user.is_staff and comment.user != request.user and comment.tweet.user != request.user:
        return HttpResponseBadRequest("You do not have permission to delete this reply.")
    tweet_id = comment.tweet_id
    comment.delete()
    messages.success(request, "Reply deleted.")
    return redirect("tweet_detail", tweet_id=tweet_id)


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    tweets = _tweet_queryset().filter(user=profile_user)
    paginator = Paginator(tweets, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "tweet/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "tweets": page_obj,
            "page_obj": page_obj,
        },
    )


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "tweet/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("tweet_list")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Welcome! Your account is ready.")
            return redirect("tweet_list")
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})

@_staff_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    author = request.GET.get("author", "").strip()

    posts = _tweet_queryset()
    if query:
        posts = posts.filter(
            Q(text_field__icontains=query)
            | Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        ).distinct()
    if author:
        posts = posts.filter(user__username__iexact=author)

    paginator = Paginator(posts, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "query": query,
        "author": author,
        "total_posts": Tweet.objects.count(),
        "total_users": User.objects.count(),
        "total_comments": Comment.objects.count(),
        "total_likes": Tweet.objects.aggregate(total=Count("likes", distinct=False))["total"] or 0,
        "latest_users": User.objects.order_by("-date_joined")[:5],
    }
    return render(request, "tweet/admin_dashboard.html", context)


@_staff_required
def admin_tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet.objects.select_related("user"), pk=tweet_id)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, f"Post #{tweet.id} updated successfully.")
            return redirect("admin_dashboard")
    else:
        form = TweetForm(instance=tweet)

    return render(
        request,
        "tweet/admin_post_form.html",
        {"form": form, "tweet": tweet},
    )


@_staff_required
def admin_tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet.objects.select_related("user"), pk=tweet_id)

    if request.method == "POST":
        post_id = tweet.id
        owner = tweet.user.username
        tweet.delete()
        messages.success(request, f"Post #{post_id} by @{owner} was deleted.")
        return redirect("admin_dashboard")

    return render(
        request,
        "tweet/admin_post_delete.html",
        {"tweet": tweet},
    )

