from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("productlist", views.Products.as_view(), name="productlist"),
    path("addoffer", views.addoffer, name="addoffer"),
    path("offerlist", views.Offers.as_view(), name="offerlist"),
    path(
        "singleproduct/<int:id_>", views.SingleProduct.as_view(), name="singleproduct"
    ),
    path("singleoffer/<int:id_>", views.SingleOffer.as_view(), name="singleoffer"),
    path("myshipments", views.myshipments, name="myshipments"),
    path("orders", views.orders, name="orders"),
    path("singleorder/<int:id_>", views.SingleOrder.as_view(), name="singleorder"),
    path("users", views.users, name="users"),
    path("register", views.register, name="signup"),
    path("loginpage", views.loginpage),
    path("login", views.StaffLogin.as_view(), name="signin"),
    path("logout", views.StaffLogout.as_view(), name="signout"),
]
