from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def productlist(request):
    return render(request, 'productlist.html', {
        "products" : [
        {
            "id": "product_1",
            "title": "DISINFECTED SOLUTION",
            "price": 300,
            "image": "images/product1.png",
            "rating": {
            "rate": 3.9,
            "count": 120
        }
        },
        {
            "id": "product_2",
            "title": "DISINFECTED SOLUTION 2",
            "price": 400,
            "image": "images/product2.png",
            "rating": {
            "rate": 3.9,
            "count": 20
        }
        },
        {
            "id": "product_3",
            "title": "DISINFECTED SOLUTION",
            "price": 300,
            "image": "images/product1.png",
            "rating": {
            "rate": 3.9,
            "count": 120
        }
        },
        {
            "id": "product_4",
            "title": "DISINFECTED SOLUTION 2",
            "price": 400,
            "image": "images/product2.png",
            "rating": {
            "rate": 3.9,
            "count": 20
        }
        },
        {
            "id": "product_5",
            "title": "DISINFECTED SOLUTION",
            "price": 300,
            "image": "images/product1.png",
            "rating": {
            "rate": 3.9,
            "count": 120
        }
        },
            {
            "id": "product_6",
            "title": "DISINFECTED SOLUTION 2",
            "price": 400,
            "image": "images/product2.png",
            "rating": {
            "rate": 3.9,
            "count": 20
        }
        },
    ]})


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
