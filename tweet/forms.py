from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Profile, Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["text_field", "photo"]
        labels = {"text_field": "", "photo": "Add a photo"}
        widgets = {
            "text_field": forms.Textarea(
                attrs={
                    "class": "form-control composer-textarea",
                    "placeholder": "What are you thinking about?",
                    "rows": 5,
                    "maxlength": 240,
                    "data-character-input": "true",
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control file-input",
                    "accept": "image/*",
                    "data-image-input": "true",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "comment-input",
                    "placeholder": "Write a thoughtful reply…",
                    "maxlength": 280,
                    "autocomplete": "off",
                }
            )
        }


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio", "location")
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "maxlength": 160,
                    "placeholder": "Tell people a little about yourself…",
                }
            ),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "City, country"}),
        }
