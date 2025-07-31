from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from django.urls.base import reverse_lazy

from users.apps import UsersConfig
from users.services import block_user

from .views import CustomLoginView, RegisterView, UserDetailView, UserListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<int:pk>/", UserUpdateView.as_view(), name="profile"),
    path("users/<int:pk>/block/", block_user, name="block_user"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
