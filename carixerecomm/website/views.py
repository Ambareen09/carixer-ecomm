import json
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def productlist(request):
    return render(request, 'productlist.html')


def waterless(request):
    return render(request, 'waterless.html')


def orders(request):
    return render(request, 'orders.html')


def ordersdetail(request):
    return render(request, 'orderdetail.html')


def checkout(request):
    return render(request, 'checkout.html')
