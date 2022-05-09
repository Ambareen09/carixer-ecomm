import json

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth.models import User

from website.serializers import ProductSerializer
from website.models import Product, OrderDetail, About, Waterless, DeliveryCheckpoint


def cartItems(request):
    cart = list(OrderDetail.objects.filter(
        user__id=request.user.id, status="INCART").values())
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


def index(request):
    # about = list(About.objects.values())
    # cart = cartItems(request)
    # products = ProductSerializer().serialize(Product.objects.all(), fields=[
    #     'id',  'title', 'price', 'image', 'featured', 'short_description', 'long_description', 'reviews'])
    # products = [p['fields'] for p in json.loads(products)]
    # for p in products:
    #     reviews = p['reviews']
    #     count = len(reviews)
    #     rates = [r['rate'] for r in reviews]
    #     p['rating'] = {'count': count, 'rate': sum(rates)/max(1, count)}
    return render(request, 'adminpanel/index.html')


def addproduct(request):
    if request.method == 'POST':
        title = request.POST.get('productname')
        productDesc = request.POST.get('description')
        image = request.POST.get('productimage')
        size = request.POST.get("size")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        priceDict = {'size': size, 'price': price, 'stock': stock}
        Product.objects.create(
            title=title, long_description=productDesc, image=image, price=priceDict)
        return HttpResponseRedirect('/adminpanel/productlist')
    if request.method == 'GET':
        return render(request, 'adminpanel/addproduct.html')


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

    return render(request, 'adminpanel/productlist.html', {
        "products": products, "cart": cart
    })


def myshipments(request):
    return render(request, 'adminpanel/myshipments.html')


def orders(request):
    return render(request, 'adminpanel/orders.html')


def users(request):
    return render(request, 'adminpanel/users.html')
