from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("tweet/", RedirectView.as_view(pattern_name="tweet_list", permanent=False)),
    path("", include("tweet.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
