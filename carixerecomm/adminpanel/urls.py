from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("productlist", views.Products.as_view(), name="productlist"),
    path(
        "singleproduct/<int:id_>", views.SingleProduct.as_view(), name="singleproduct"
    ),
    path("myshipments", views.myshipments, name="myshipments"),
    path("orders", views.orders, name="orders"),
    path("singleorder/<int:id_>", views.SingleOrder.as_view(), name="singleorder"),
    path("users", views.users, name="users"),
    path("register", views.register, name="signup"),
    path("loginpage", views.loginpage),
    path("login", views.StaffLogin.as_view(), name="signin"),
    path("logout", LogoutView.as_view(), name="signout"),
]
