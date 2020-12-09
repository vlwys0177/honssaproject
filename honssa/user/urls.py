from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path("login/",login_view, name="login"),
    path("logout/",logout_view , name="logout"),
    path("signup/",signup_view, name="signup"),
    path("find_id/",find_id, name="find_id"),
    path("find_password/",find_password, name="find_password")
]