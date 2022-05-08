import json
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth.models import User

from .serializers import ProductSerializer
from .models import Product, OrderDetail, About, Waterless, DeliveryCheckpoint

def register(request):
    data = request.POST
    username = data['username']
    password = data['password']
    email = data['email']

    if User.objects.filter(username=username).exists():
        return index(request)
    
    if User.objects.filter(email=email).exists():
        return index(request)

    user = User.objects.create_user(username=username, email=email, password=password)
    return index(request)
    

def cartItems(request):
    cart = list(OrderDetail.objects.filter(status="INCART").values())
    for o in cart:
        product = list(Product.objects.filter(id=o['product_id']).values())
        for p in product:
            o['title'] = p['title']
            o['image'] = p['image']
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
    return cart


def cart(cartItems):
    cartList = {'grandTotal': 0}
    print(cartItems)
    for c in cartItems:
        cartList['grandTotal'] += c['totalPrice']
    return cartList


def index(request):
    about = list(About.objects.values())
    cart = cartItems(request)
    products = ProductSerializer().serialize(Product.objects.all(), fields=[
        'id',  'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    for p in products:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}
    return render(request, 'index.html', {
        "products": products, "about": about, "cart": cart
    })


def about(request):
    about = list(About.objects.values())
    cart = cartItems(request)
    return render(request, 'about.html', {'about': about, "cart": cart})


def productlist(request):
    products = ProductSerializer().serialize(Product.objects.all(), fields=[
        'id',   'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    products = [p['fields'] for p in json.loads(products)]
    cart = cartItems(request)
    for p in products:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    return render(request, 'productlist.html', {
        "products": products, "cart": cart
    })


def waterless(request):
    waterless = list(Waterless.objects.values())
    cart = cartItems(request)
    print(waterless)
    return render(request, 'waterless.html', {"waterless": waterless, "cart": cart})


def orders(request):
    orders = list(OrderDetail.objects.exclude(status="INCART").values())
    cart = cartItems(request)
    for o in orders:
        product = list(Product.objects.filter(id=o['product_id']).values())
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
    return render(request, 'orders.html', {"orders": orders, "cart": cart})


def ordersdetail(request, id):
    orders = list(OrderDetail.objects.filter(id=id).values())
    cart = cartItems(request)
    for o in orders:
        product = list(Product.objects.filter(id=o['product_id']).values())
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
        o['checkpoints'] = [model_to_dict(c) for c in DeliveryCheckpoint.objects.filter(order__id=id).order_by("transit_index")]
    return render(request, 'orderdetail.html', {"orders": orders, "cart": cart})


def checkout(request):
    cartItem = cartItems(request)
    carts = cart(cartItem)
    return render(request, 'checkout.html', {"cartItems": cartItem, "cart": carts})


def productdetail(request, id):
    cart = cartItems(request)
    product = ProductSerializer().serialize(Product.objects.filter(pk=id), fields=[
        'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    suggestions = ProductSerializer().serialize(Product.objects.all(), fields=[
        'id',   'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    product = [p['fields'] for p in json.loads(product)]
    suggestions = [p['fields'] for p in json.loads(suggestions)]
    for p in product:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    for p in suggestions:
        reviews = p['reviews']
        count = len(reviews)
        rates = [r['rate'] for r in reviews]
        p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}

    return render(request, 'productdetail.html', {
        "p": product[0], "suggestions": suggestions, "cart": cart
    })
