import json

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .forms import UploadProduct

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

def loginpage(request):
    return render(request, 'adminpanel/login.html')

class StaffForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
        if not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name}
            )

class StaffLogin(LoginView):
    form_class = AuthenticationForm
    template_name = "adminpanel/login.html"



def index(request):
    user = request.user
    if not (user.is_authenticated and user.is_active and user.is_staff):
        return redirect('/panel/login')
    return render(request, 'adminpanel/index.html')


class Products(View):
    def post(self, request):
        title = request.POST.get('productname')
        product_desc = request.POST.get('description')
        image = request.POST.get('productimage')
        size = request.POST.get("size")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        if Product.objects.filter(title=title, size=size).exists():
            return HttpResponseRedirect('/panel/productlist')

        Product.objects.create(
            title=title, long_description=product_desc, image=image, price=price, size=size, stock=stock)
        return HttpResponseRedirect('/panel/productlist')
    
    def get(self, request):
        query_products = Product.objects.all()
        products = ProductSerializer().serialize(query_products, fields=[
            'id', 'title', 'size', 'price', 'stock', 'image', 'featured', 'short_description', 'long_description', 'reviews', 'status'])

        products = [p['fields'] for p in json.loads(products)]
        return render(request, 'adminpanel/productlist.html', {
                    "products": products
                })
    
    # def put(self, request):


class SingleProduct(View):
    def put(self, request, id_):
        if Product.objects.filter(id=id_).exists():
            p = Product.objects.get(id=id_)
            p.save()
        return HttpResponse({'msg': 'successful'})
        
    def delete(self, request, id_):
        if Product.objects.filter(id=id_).exists():
            Product.objects.get(id=id_).delete()
        return HttpResponse({'msg': 'successful'})

def addproduct(request):
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
