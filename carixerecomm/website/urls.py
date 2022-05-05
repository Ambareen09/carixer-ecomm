from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('about', views.about, name='about'),
    path('productlist', views.productlist, name='product-list'),
    path('waterless', views.waterless, name='waterless'),
    path('orders', views.orders, name='orders'),
    path('orderdetail', views.ordersdetail, name='order-detail'),
    path('checkout', views.checkout, name='checkout'),
    path('productdetail', views.productdetail, name='product-detail'),

]
