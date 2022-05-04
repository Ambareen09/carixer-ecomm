import json
from django.shortcuts import render
from .serializers import ProductSerializer
from .models import Product

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def productlist(request):
    products = ProductSerializer().serialize(Product.objects.all(), fields=['title', 'price', 'image', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    for p in products:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    return render(request, 'productlist.html', {
        "products" : products
        })


def waterless(request):
    return render(request, 'waterless.html')


def orders(request):
    return render(request, 'orders.html')


def ordersdetail(request):
    return render(request, 'orderdetail.html')


def checkout(request):
    return render(request, 'checkout.html')

def productdetail(request):
    return render(request, 'productdetail.html')
