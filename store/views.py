from django.shortcuts import get_object_or_404, render
from .models import *


def home(request):
    context = {}
    return render(request, 'store/home.html', context)


def store(request):

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)
