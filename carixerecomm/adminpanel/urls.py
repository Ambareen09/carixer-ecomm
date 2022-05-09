from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("productlist", views.productlist, name="productlist"),
    path("myshipments", views.myshipments, name="myshipments"),
    path("orders", views.orders, name="orders"),
    path("users", views.users, name="users"),

    path("register", views.register, name="signup"),
    path("login", LoginView.as_view(), name="signin"),
    path("logout", LogoutView.as_view(), name="signout"),
]
