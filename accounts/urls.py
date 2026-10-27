from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import register, CustomLoginView, CustomLogoutView


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]