import json
import re

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.gis.geoip2 import GeoIP2

from .serializers import ProductSerializer
from .models import (
    Product,
    OrderDetail,
    About,
    Waterless,
    DeliveryCheckpoint,
    Profile,
    OfferBanner,
)


def register(request):
    data = request.POST
    username = data["username"]
    password = data["password"]
    email = data.get("email", "")
    phone_number = data.get("phone_number", "")

    if User.objects.filter(username=username).exists():
        messages.error(request, "user with username already exists")
        return redirect("/")

    if email:
        if Profile.objects.filter(email=email).exists():
            messages.error(request, "user with this email already exists")
            return redirect("/")
    elif phone_number:
        if Profile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "user with this phone number already exists")
            return redirect("/")
    else:
        messages.error(request, "please provide either email or phone number")
        return redirect("/")

    user = User.objects.create_user(username=username, email=email, password=password)
    Profile.objects.create(user=user, email=email, phone_number=phone_number)
    messages.success(request, "account successfully created")
    return redirect("/")


class UserLogin(View):
    def post(self, request):
        data = request.POST
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        g = GeoIP2()

        if user:
            if user.is_active:
                login(request, user)
                profile = Profile.objects.get(user=user)
                # profile.location = g.country(request.META["REMOTE_ADDR"])
                profile.save()
                messages.success(request, "login succesful")
            else:
                messages.error(request, "inactive account")
        else:
            messages.error(request, "invalid credentials")
        return HttpResponseRedirect(request.headers["Referer"])


def cartItems(request, ids=None):
    if ids:
        cart = list(
            OrderDetail.objects.filter(
                id__in=ids, user__id=request.user.id, status="INCART"
            ).values()
        )
    else:
        cart = list(
            OrderDetail.objects.filter(
                user__id=request.user.id, status="INCART"
            ).values()
        )
    for o in cart:
        p = Product.objects.get(id=o["product_id"])
        o["title"] = p.title
        o["image"] = str(p.image)
        o["price"] = p.price
        o["totalPrice"] = o["quantity"] * p.price
        o["save"] = o["totalPrice"] + 0.5 * o["totalPrice"]
        o["percentSave"] = 50
        temp = o["status"]
        o["status_color"] = ""
        if temp == "DELIVERED":
            o["status_color"] = "delivery"
        elif temp == "ORDERED":
            o["status_color"] = "order"
        elif temp == "CANCELLED":
            o["status_color"] = "cancel"
        else:
            o["status_color"] = "cancel"
    return cart


def cart(cartItems):
    cartList = {"grandTotal": 0}
    for c in cartItems:
        cartList["grandTotal"] += c["totalPrice"]
    return cartList


def index(request):
    about = list(About.objects.values())
    cart = cartItems(request)
    products = ProductSerializer().serialize(
        Product.objects.filter(featured=True),
        fields=[
            "id",
            "title",
            "price",
            "image",
            "featured",
            "short_description",
            "long_description",
            "reviews",
        ],
    )
    products = [p["fields"] for p in json.loads(products)]
    for p in products:
        reviews = p["reviews"]
        count = len(reviews)
        rates = [r["rate"] for r in reviews]
        p["rating"] = {"count": count, "rate": sum(rates) / max(1, count)}

    banners = [model_to_dict(b) for b in OfferBanner.objects.all()]
    return render(
        request,
        "index.html",
        {"products": products, "about": about, "cart": cart, "banners": banners},
    )


def about(request):
    about = list(About.objects.values())
    cart = cartItems(request)
    return render(request, "about.html", {"about": about, "cart": cart})


def productlist(request):
    query_products = Product.objects.exclude(status="DRAFT")
    if "search" in request.GET:
        query_products = query_products.filter(title__icontains=request.GET["search"])
        if "sort" in request.GET:
            query_products = query_products.order_by(
                ("-" if request.GET["sort"] == "desc" else "") + "price"
            )
    elif "sort" in request.GET:
        query_products = query_products.order_by(
            ("-" if request.GET["sort"] == "desc" else "") + "price"
        )
    products = ProductSerializer().serialize(
        query_products,
        fields=[
            "id",
            "title",
            "price",
            "image",
            "featured",
            "short_description",
            "long_description",
            "reviews",
        ],
    )
    products = [p["fields"] for p in json.loads(products)]
    cart = cartItems(request)
    for p in products:
        reviews = p["reviews"]
        count = len(reviews)
        rates = [r["rate"] for r in reviews]
        p["rating"] = {"count": count, "rate": sum(rates) / max(1, count)}

    return render(request, "productlist.html", {"products": products, "cart": cart})


def offers(request):
    query_products = Product.objects.exclude(status="DRAFT").filter(discount__gt=0)
    if "search" in request.GET:
        query_products = query_products.filter(title__icontains=request.GET["search"])
        if "sort" in request.GET:
            query_products = query_products.order_by(
                ("-" if request.GET["sort"] == "desc" else "") + "price"
            )
    elif "sort" in request.GET:
        query_products = query_products.order_by(
            ("-" if request.GET["sort"] == "desc" else "") + "price"
        )
    products = ProductSerializer().serialize(
        query_products,
        fields=[
            "id",
            "title",
            "price",
            "discount",
            "image",
            "featured",
            "short_description",
            "long_description",
            "reviews",
        ],
    )
    products = [p["fields"] for p in json.loads(products)]
    cart = cartItems(request)
    for p in products:
        reviews = p["reviews"]
        count = len(reviews)
        rates = [r["rate"] for r in reviews]
        p["rating"] = {"count": count, "rate": sum(rates) / max(1, count)}

    return render(request, "offerlist.html", {"products": products, "cart": cart})


def waterless(request):
    waterless = list(Waterless.objects.values())
    cart = cartItems(request)
    print(waterless)
    return render(request, "waterless.html", {"waterless": waterless, "cart": cart})


def orders(request):
    orders = list(OrderDetail.objects.exclude(status="INCART").values())
    cart = cartItems(request)
    for o in orders:
        product = list(Product.objects.filter(id=o["product_id"]).values())
        for p in product:
            o["title"] = p["title"]
            o["size"] = p["size"]
            o["totalPrice"] = o["quantity"] * p["price"]
            o["save"] = o["totalPrice"] + 0.5 * o["totalPrice"]
        o["percentSave"] = 50
        temp = o["status"]
        o["status_color"] = ""
        if temp == "DELIVERED":
            o["status_color"] = "delivery"
        elif temp == "ORDERED":
            o["status_color"] = "order"
        elif temp == "CANCELLED":
            o["status_color"] = "cancel"
        else:
            o["status_color"] = "order"
    return render(request, "orders.html", {"orders": orders, "cart": cart})


def ordersdetail(request, id):
    orders = list(OrderDetail.objects.filter(id=id).values())
    cart = cartItems(request)
    for o in orders:
        product = list(Product.objects.filter(id=o["product_id"]).values())
        for p in product:
            o["title"] = p["title"]
            o["size"] = p["size"]
            o["totalPrice"] = o["quantity"] * p["price"]
            o["save"] = o["totalPrice"] + 0.5 * o["totalPrice"]
        o["percentSave"] = 50
        temp = o["status"]
        o["status_color"] = ""
        if temp == "DELIVERED":
            o["status_color"] = "delivery"
        elif temp == "ORDERED":
            o["status_color"] = "order"
        elif temp == "CANCELLED":
            o["status_color"] = "cancel"
        else:
            o["status_color"] = "cancel"
        o["checkpoints"] = [
            model_to_dict(c)
            for c in DeliveryCheckpoint.objects.filter(order__id=id).order_by(
                "transit_index"
            )
        ]
    return render(request, "orderdetail.html", {"orders": orders, "cart": cart})


def checkout(request):
    if request.method == "POST":
        country = request.POST.get("country")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        address = request.POST.get("address")
        apartment = request.POST.get("apartment")
        postal_code = request.POST.get("postalcode")
        city = request.POST.get("city")
        phone_number = request.POST.get("phonenumber")
        shipping_charge = request.POST.get("flexRadioDefault")

        for odo in OrderDetail.objects.filter(
            user__id=request.user.id, status="INCART"
        ):
            odo.country = country
            odo.first_name = first_name
            odo.last_name = last_name
            odo.address = address
            odo.apartment = apartment
            odo.postal_code = postal_code
            odo.city = city
            odo.phone_number = phone_number
            odo.shipping_charge = shipping_charge
            odo.status = "ORDERED"
            odo.save()
        return HttpResponseRedirect("/productlist")

    if request.method == "GET":
        items = request.GET.get("items", None)
        ids = None
        if items:
            ids = list(map(int, json.loads(items)))
        cartItem = cartItems(request, ids)
        carts = cart(cartItem)
        return render(request, "checkout.html", {"cartItems": cartItem, "cart": carts})


def productdetail(request, id):
    cart = cartItems(request)
    product = Product.objects.get(id=id)
    product = ProductSerializer().serialize(
        Product.objects.filter(title=product.title),
        fields=[
            "id",
            "title",
            "size",
            "price",
            "image",
            "featured",
            "short_description",
            "long_description",
            "reviews",
        ],
    )
    suggestions = ProductSerializer().serialize(
        Product.objects.exclude(title=product.title),
        fields=[
            "id",
            "title",
            "price",
            "image",
            "featured",
            "short_description",
            "long_description",
            "reviews",
        ],
    )
    product = [p["fields"] for p in json.loads(product)]
    suggestions = [p["fields"] for p in json.loads(suggestions)]
    for p in product:
        reviews = p["reviews"]
        print(reviews)
        count = len(reviews)
        rates = [r["rate"] for r in reviews]
        p["rating"] = {"count": count, "rate": sum(rates) / max(1, count)}

    for p in suggestions:
        reviews = p["reviews"]
        count = len(reviews)
        rates = [r["rate"] for r in reviews]
        p["rating"] = {"count": count, "rate": sum(rates) / max(1, count)}

    sizes = [{"id": p["id"], "price": p["price"], "size": p["size"]} for p in product]
    print(sizes)
    return render(
        request,
        "productdetail.html",
        {"p": product[0], "sizes": sizes, "suggestions": suggestions, "cart": cart},
    )


class cartView(View):
    def put(self, request, id_):
        data = json.loads(request.body.decode("utf-8"))
        odo = OrderDetail.objects.get(id=id_, user__id=request.user.id, status="INCART")
        if data["quantity"] > 0:
            odo.quantity = data["quantity"]
            odo.save()
        else:
            odo.delete()
        return HttpResponse({"msg": "successful"})

    def post(self, request, id_):
        data = json.loads(request.body.decode("utf-8"))
        from datetime import date

        if OrderDetail.objects.filter(
            product__id=id_, user__id=request.user.id, status="INCART"
        ).exists():
            odo = OrderDetail.objects.get(
                product__id=id_, user__id=request.user.id, status="INCART"
            )
            odo.quantity += data["quantity"]
            odo.save()
        else:
            odo = OrderDetail(
                user=request.user,
                status="INCART",
                date=date.today(),
                product=Product.objects.get(id=id_),
                quantity=data["quantity"],
            )
            odo.save()
        return HttpResponse({"msg": "successful"})
