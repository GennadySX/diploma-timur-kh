from django.shortcuts import render
from web.models import Product

def index(request):
    return render(request, 'web/index.html')

def shop(request):
    product = Product.objects.all()
    context = {
        'pr': product
    }
    return render(request, 'web/shop.html', context)

def cart(request):
    product = Product.objects.all()[:2]
    context = {
        'pr': product
    }
    return render(request, 'web/cart.html', context)
