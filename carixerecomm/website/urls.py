from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('about.html', views.about, name='about'),
    path('productlist.html', views.productlist, name='product-list'),
    path('waterless.html', views.waterless, name='waterless'),
    path('orders.html', views.orders, name='orders'),
    path('orderdetail.html', views.ordersdetail, name='order-detail'),
    path('checkout.html', views.checkout, name='checkout'),
    path('productdetail.html', views.productdetail, name='product-detail'),

]
