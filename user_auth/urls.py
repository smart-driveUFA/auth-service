from django.urls import path

from user_auth.views import login_view, profile, verify_token, create_super_user

app_name = "user_auth"

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", login_view, name="login"),
    path("create_super_user/", create_super_user, name="create_super_user"),
    path("verify_token/", verify_token, name="verify_token"),
]
