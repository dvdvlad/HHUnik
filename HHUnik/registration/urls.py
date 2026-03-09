from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'registration'
urlpatterns = [
    path("", views.Registr.as_view(), name="Registration"),
    path("logout/", LogoutView.as_view(), name="Logout"),
    path("login/", views.LoginUser.as_view(), name="Login"),
]
