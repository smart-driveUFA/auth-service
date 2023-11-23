from django.urls import path

from user_auth.views import create_super_user, login_view, profile

app_name = "user_auth"

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", login_view, name="login"),
    path("create_super_user/", create_super_user, name="create_super_user"),
]
