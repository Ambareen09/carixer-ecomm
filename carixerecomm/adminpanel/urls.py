from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
     path("", views.index),
    
    path("register", views.register, name="signup"),
    path("login", LoginView.as_view(), name="signin"),
    path("logout", LogoutView.as_view(), name="signout"),
]
