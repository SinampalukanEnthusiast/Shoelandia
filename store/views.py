from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from store.forms import *

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    context = {}
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

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {'product': product}
    return render(request, 'store/product_detail.html', context)
