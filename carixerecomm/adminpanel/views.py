import json

from django.views import View
from django.http import HttpResponse
from django.forms import model_to_dict
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import UploadProduct

from website.serializers import ProductSerializer
from website.models import Product, OrderDetail, About, Waterless, DeliveryCheckpoint


# def cartItems(request):
#     cart = list(OrderDetail.objects.filter(
#         user__id=request.user.id, status="INCART").values())
#     for o in cart:
#         product = list(Product.objects.filter(id=o['product_id']).values())
#         for p in product:
#             o['title'] = p['title']
#             o['image'] = p['image']
#             o['totalPrice'] = o['quantity']*p['price']
#             o['save'] = o['totalPrice'] + 0.5*o['totalPrice']
#         o['percentSave'] = 50
#         temp = (o['status'])
#         o['status_color'] = ""
#         match temp:
#             case "DELIVERED":
#                 o['status_color'] = "delivery"
#             case "ORDERED":
#                 o['status_color'] = "order"
#             case "CANCELLED":
#                 o['status_color'] = "cancel"
#             case default:
#                 o['status_color'] = "cancel"
#     return cart


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
    if request.POST:
        form = UploadProduct(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'adminpanel/addproduct.html', {'form': form})


def productlist(request):
    return render(request, 'adminpanel/productlist.html')


def myshipments(request):
    return render(request, 'adminpanel/myshipments.html')


def orders(request):
    return render(request, 'adminpanel/orders.html')


def users(request):
    return render(request, 'adminpanel/users.html')
