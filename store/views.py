from re import sub
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.db.models import Count


def home(request):
    category_data = Category.objects.all()
    products_data = Product.objects.all()
    sub_product = SubProduct.objects.filter().values('sub_name', 'product')
    # print(products_data.subproduct_set.all())
    context = {'category_data': category_data,
               "products_data": products_data, "sub_product": sub_product}
    return render(request, 'store/home.html', context)


def store(request):

    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def get_practice(request):
    category_data = Category.objects.all()
    products_data = Product.objects.all()
    sub_product = SubProduct.objects.filter().values('sub_name', 'product')
    # print(products_data.subproduct_set.all())
    context = {'category_data': category_data,
               "products_data": products_data, "sub_product": sub_product}
    return render(request, 'store/categories.html', context)


def product_detail(request, slug):
    """Reverse searches subproducts from product object.
    """

    # todo, make detail image reflective of selected option,
    # make summary image reflective of option
    # make order page mockup
    ##
    color_get = []
    sizes = []
    if request.GET:
        for value in request.GET.values():
            print(f'request.get: {value[0:2]}')
            color_get.append(value)

    print(color_get)
    color_selected = None
    product = get_object_or_404(Product, slug=slug)
    product_sets = product.get_subproducts()
    colors = SubProduct.objects.filter(
        product__slug=slug).values('sub_name', 'productcolor__color',  'is_default')
    if color_get:
        color_selected = SubProduct.objects.filter(
            product__slug=slug).filter(productcolor__color__in=color_get).values('sub_name',).annotate(is_selected=Count('sub_name'))
        print(f'color selected: {color_selected}')
        sizes = ProductSizes.objects.filter(
            sub_product__sub_name=color_selected[0]['sub_name']).filter(sub_product__productcolor__color__in=color_get).values('size', 'stock_amount', 'sub_product__sub_name')

    else:
        choices = ProductSizes.SIZE_CHOICES
        for size in choices:
            sizes.append({'size': size[0]})
    print(f'sub products in colors: {colors}')
    featured_image = None

    try:
        total_stock = 0
        for stock in sizes:
            total_stock += stock['stock_amount']
    except:
        total_stock = 0
    if sizes:
        print(
            f'~~~colors: {colors},\n~~~sizes: {sizes},\n~~~~total_stock: {total_stock}')
    else:
        print("no sizes:~~~~~~~~~")
    stock = []

    # refactor to use .filter instead
    for subproduct in product_sets:
        if subproduct.is_default:
            images = subproduct.get_images()
            featured_image = subproduct.get_featured(images)
            print(featured_image)
    ###########

    if color_get:
        context = {'product': product, 'image': featured_image,
                   'sizes': sizes, 'stock': total_stock, 'colors': colors, 'color_selected': color_selected, 'variant': color_get[0]}
    else:

        context = {'product': product, 'image': featured_image,
                   'sizes': sizes, 'stock': total_stock, 'colors': colors, 'color_selected': color_selected, }
    return render(request, 'store/product_detail.html', context)


def category_products(request, category):
    data = Product.objects.filter(
        category__slug=category).values('title', 'slug')
    print(f'data: {data}')
    context = {"data": data}
    return render(request, 'store/category_products.html', context)
