from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("", views.index),
    
    path("register", views.register, name="signup"),
    path("login", LoginView.as_view(), name="signin"),
    path("login", LogoutView.as_view(), name="signout"),
    
    path('about', views.about, name='about'),
    path('productlist', views.productlist, name='product-list'),
    path('waterless', views.waterless, name='waterless'),
    path('orders', views.orders, name='orders'),
    path('orderdetail/<int:id>', views.ordersdetail, name='order-detail'),
    path('checkout', views.checkout, name='checkout'),
    path('productdetail/<int:id>', views.productdetail, name='product-detail'),

]
