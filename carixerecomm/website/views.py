from email.policy import default
import json
from tkinter.tix import Form
from django.forms import model_to_dict
from django.shortcuts import render
from django.core.serializers import serialize
from .serializers import ProductSerializer
from .models import Product, OrderDetail, About


def index(request):
    about = list(About.objects.values())
    products = ProductSerializer().serialize(Product.objects.all(), fields=[
        'id',  'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    for p in products:
        p['id'] = id
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}
    return render(request, 'index.html', {
        "products": products, "about": about
    })


def about(request):
    about = list(About.objects.values())
    return render(request, 'about.html', {'about': about})


def productlist(request):
    products = ProductSerializer().serialize(Product.objects.all(), fields=[
        'id',   'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    for p in products:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    return render(request, 'productlist.html', {
        "products": products
    })


def waterless(request):
    return render(request, 'waterless.html')


def orders(request):
    orders = list(OrderDetail.objects.values())
    for o in orders:
        product = list(Product.objects.values())
        for p in product:
            o['title'] = p['title']
            o['totalPrice'] = o['quantity']*p['price']
            o['save'] = o['totalPrice'] + 0.5*o['totalPrice']
        o['percentSave'] = 50
        temp = (o['status'])
        o['status_color'] = ""
        match temp:
            case "DELIVERED":
                o['status_color'] = "delivery"
            case "ORDERED":
                o['status_color'] = "order"
            case "CANCELLED":
                o['status_color'] = "cancel"
            case default:
                o['status_color'] = "cancel"
        print(o['status_color'])
    return render(request, 'orders.html', {"orders": orders})


def ordersdetail(request):
    return render(request, 'orderdetail.html')


def checkout(request):
    return render(request, 'checkout.html')


def productdetail(request, id):
    products = ProductSerializer().serialize(Product.objects.filter(pk=id).order_by('title')[:5], fields=[
        'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    for p in products:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    return render(request, 'productdetail.html', {
        "products": products
    })
