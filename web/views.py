from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from web.models import *

from django.db.models.aggregates import Sum
from users.forms import *

from web.models import *


def index(request):
    comments = Comments.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'web/index.html', {'comments': comments})


def comments(request):
    return render(request, 'web/comments.html')
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'


def shop(request):
    product = Product.objects.all()
    context = {
        'pr': product
    }
    return render(request, 'web/shop.html', context)


@login_required(login_url='/login/')
def cart(request):
    if not request.user:
        return redirect('login')
    cart_object, _ = Cart.objects.get_or_create(created_by=request.user, cart__pay=None)
    context = {
        'cart': cart_object,
        'price': cart_object.price,
        'price_total': cart_object.price + 250,
    }
    return render(request, 'web/cart.html', context)


@csrf_exempt
def add_to_cart(request, **kwargs):
    if not request.user.id:
        return JsonResponse({'success': False, 'url': '/login/'})
    cart_object, _ = Cart.objects.get_or_create(created_by=request.user, cart__pay=None)
    product = Product.objects.get(**kwargs)
    if CartEntry.objects.filter(cart=cart_object, product=product).exists():
        cart_entry = CartEntry.objects.get(cart=cart_object, product=product)
        cart_entry.count += 1
        if not cart_entry.count > product.available_count:
            cart_entry.save()
    else:
        if product.available_count >= 1:
            CartEntry.objects.create(cart=cart_object, product=product, count=1)

    return JsonResponse({'success': True})


@login_required(login_url='/login/')
def delete_from_cart(request, **kwargs):
    if not request.user:
        return redirect('login')
    product = Product.objects.get(**kwargs)
    cart_entry = CartEntry.objects.get(cart__created_by=request.user, cart__cart__pay=None, product=product)
    if cart_entry.count == 1:
        cart_entry.delete()
    else:
        cart_entry.count -= 1
        cart_entry.save()
    return redirect('cart')


@login_required(login_url='/login/')
def pay(request, **kwargs):
    if not request.user:
        return redirect('login')
    cart_object = Cart.objects.get(created_by=request.user, cart__pay=None)
    Pay.objects.create(
        cart_id=cart_object,
        created_by=request.user,
        fullName=request.POST.get('fullName'),
        number=request.POST.get('number', ''),
        address=request.POST.get('address', ''),
        pay=request.POST.get('pay', 0),
        delivery=request.POST.get('delivery', 0),
    )
    set_all = cart_object.cartentry_set.all()
    for cart_entry in set_all:
        p: Product = Product.objects.get(cartentry=cart_entry)
        p.available_count -= cart_entry.count
        p.save()
    return redirect('shop')
