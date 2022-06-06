from itertools import product
from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from store.forms import *

from .models import *
from .utils import cookie_cart, cart_data, guest_order

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'store/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterUser()
        if request.method == 'POST':
            form = RegisterUser(request.POST)
            if form.is_valid():
                form.save()
                customer_username = form.cleaned_data['username']
                customer_name = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
                email = form.cleaned_data['email']
                user = User.objects.get(username=customer_username)
                customer = Customer.objects.create(
                    name=customer_name, email=email)
                customer.user = user
                customer.save()
                messages.success(request, "Account created!")
                return redirect('login')
        context = {'form': form}
        return render(request, 'store/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account logged in!")
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect!')
        context = {'form': LoginForm()}
        return render(request, 'store/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def store(request):

    data = cart_data(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # .orderitem_set.all() is sort of a reverse lookup that grabs all the orderitem classes associated
        # to this particular Order class referenced above.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):

    data = cart_data(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='login')
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(' ')
    print('Action: ', action)
    print('ProductId: ', productId)

    customer = request.user.customer
    # These are loaded from models.py
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
@csrf_exempt  # there is a video on a potential better solution to this
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    print('request body: ', request.body)
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment complete!', safe=False)


def product_detail(request, slug):
    data = cart_data(request)
    product = get_object_or_404(Product, slug=slug)
    cartItems = data['cartItems']

    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/product_detail.html', context)
