from django.urls import path

from user_auth.views import login_view, profile, verify_token

app_name = "user_auth"

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", login_view, name="login"),
    path("verify_token/", verify_token, name="verify_token"),
]
