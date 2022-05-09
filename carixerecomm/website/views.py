import json
import re

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
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

    user = User.objects.create_user(
        username=username, email=email, password=password)
    return index(request)


def cartItems(request):
    cart = list(OrderDetail.objects.filter(
        user__id=request.user.id, status="INCART").values())
    for o in cart:
        p = Product.objects.get(id=o['product_id'])
        o['title'] = p.title
        o['image'] = str(p.image)
        o['price'] = p.price
        o['totalPrice'] = o['quantity']*p.price
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
    if 'search' in request.GET:
        query_products = Product.objects.filter(
            title__icontains=request.GET['search'])
        if 'sort' in request.GET:
            query_products = query_products.order_by(
                ('-' if request.GET['sort'] == 'desc' else '')+'price')
    elif 'sort' in request.GET:
        query_products = Product.objects.all().order_by(
            ('-' if request.GET['sort'] == 'desc' else '')+'price')
    else:
        query_products = Product.objects.all()
    products = ProductSerializer().serialize(query_products, fields=[
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
            o['size'] = p['size']
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
            o['size'] = p['size']
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
        o['checkpoints'] = [model_to_dict(c) for c in DeliveryCheckpoint.objects.filter(
            order__id=id).order_by("transit_index")]
    return render(request, 'orderdetail.html', {"orders": orders, "cart": cart})


def checkout(request):
    if request.method == 'POST':
        user_id = request.user
        country = request.POST.get('country')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        address = request.POST.get('address')
        apartment = request.POST.get('apartment')
        postal_code = request.POST.get('postalcode')
        city = request.POST.get('city')
        phone_number = request.POST.get('phonenumber')
        shipping_charge = request.POST.get('flexRadioDefault')
        status = "ORDERED"

        OrderDetail.objects.create(user=user_id, country=country, first_name=first_name, last_name=last_name,
                                   address=address, apartment=apartment, postal_code=postal_code, city=city, phone_number=phone_number,
                                   shipping_charge=shipping_charge, status=status)
        return HttpResponseRedirect('/productlist')

    if request.method == 'GET':
        cartItem = cartItems(request)
        carts = cart(cartItem)
        return render(request, 'checkout.html', {"cartItems": cartItem, "cart": carts})


def productdetail(request, id):
    cart = cartItems(request)
    product = Product.objects.get(id=id)
    product = ProductSerializer().serialize(Product.objects.filter(title=product.title), fields=[
        'id', 'title', 'size', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
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

    sizes = [{'id': p['id'], 'price':p['price'], 'size': p['size']}
             for p in product]
    print(sizes)
    return render(request, 'productdetail.html', {
        "p": product[0], "sizes": sizes, "suggestions": suggestions, "cart": cart
    })


class cartView(View):
    def put(self, request, id_):
        data = json.loads(request.body.decode('utf-8'))
        odo = OrderDetail.objects.get(
            id=id_, user__id=request.user.id, status="INCART")
        if data['quantity'] > 0:
            odo.quantity = data['quantity']
            odo.save()
        else:
            odo.delete()
        return HttpResponse({'msg': 'successful'})

    def post(self, request, id_):
        data = json.loads(request.body.decode('utf-8'))
        from datetime import date
        if OrderDetail.objects.filter(product__id=id_, user__id=request.user.id, status="INCART").exists():
            odo = OrderDetail.objects.get(
                product__id=id_, user__id=request.user.id, status="INCART")
            odo.quantity += data['quantity']
            odo.save()
        else:
            odo = OrderDetail(user=request.user, status="INCART", date=date.today(),
                              product=Product.objects.get(id=id_), quantity=data['quantity'])
            odo.save()
        return HttpResponse({'msg': 'successful'})
