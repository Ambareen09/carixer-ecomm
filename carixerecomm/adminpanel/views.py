from django.shortcuts import render
from django.contrib.auth.models import User


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

