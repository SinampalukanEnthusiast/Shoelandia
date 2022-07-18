from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages


def home(request):
    category_data = Category.objects.all()
    products_data = Product.objects.all()
    sub_product = SubProduct.objects.filter().values('sub_name', 'product')
    # print(products_data.subproduct_set.all())
    context = {'category_data': category_data,
               "products_data": products_data, "sub_product": sub_product}
    return render(request, 'store/home.html', context)


def store(request):
    category_query = request.GET.getlist('category')
    search_query = request.GET.get('search')
    # color_query = request.GET.getlist('color')
    # color_query = request.GET.getlist('price')
    print(f'search query: {search_query}')

    if category_query:
        category_selected = Category.objects.filter(
            product__category__slug__in=category_query).values('slug')
        products = Product.objects.filter(
            category__slug__in=category_query)
        search_query = None
        if not products:
            messages.success(request, "No matching product found")

    elif search_query:
        products = Product.objects.filter(
            Q(description__search=search_query) | Q(title__search=search_query))
        category_selected = None
        if not products:
            messages.success(
                request, f'No matching product found for "{search_query}"')
    else:
        products = Product.objects.all()
        category_selected = None
        search_query = None

    category_data = Category.objects.filter().values('name', 'slug', )
    print(f'category : {category_selected}')
    print(f'products data : {products}')

    context = {'products': products, 'category_selected': category_selected,
               'category_data': category_data, }
    return render(request, 'store/store.html', context)


def get_practice(request):
    category_data = Category.objects.all()
    products_data = Product.objects.all()
    sub_product = SubProduct.objects.filter().values('sub_name', 'product')
    context = {'category_data': category_data,
               "products_data": products_data, "sub_product": sub_product}
    return render(request, 'store/categories.html', context)


def product_detail(request, slug):
    """Reverse searches variants, images, sizes from product object.
    """
    color_get = []
    sizes = []
    if request.GET:
        for value in request.GET.values():
            print(f'request.get: {value[0:2]}')
            color_get.append(value)

    print(color_get)
    color_selected = None
    product = get_object_or_404(Product, slug=slug)
    colors = SubProduct.objects.filter(
        product__slug=slug).values('sub_name', 'productcolor__color',  'is_default', 'product__category__name')
    product_category = colors[0]['product__category__name']
    print(f'OUTCAT: {product_category}')
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
    featured_image = None

    try:
        if color_get:
            image = ProductImage.objects.get(
                sub_product__productcolor__color=color_get[0], sub_product__product__slug=slug, )
        else:
            image = ProductImage.objects.get(
                sub_product__product__slug=slug, sub_product__is_default=True, is_feature=True)
    except:
        image = None

    print(f'imageasdsas: {type(image)}')

    related_items = Product.objects.filter(
        category__name=product_category).filter(subproduct__is_default=True).values("subproduct__product__slug", "subproduct__product_image__image")
    print(f"RELATEDITEMS: {related_items}")
    if color_get:
        context = {'product': product, 'image': image,
                   'sizes': sizes, 'stock': total_stock, 'colors': colors, 'color_selected': color_selected, 'variant': color_get[0], 'related_items': related_items}
    else:

        context = {'product': product, 'image': image,
                   'sizes': sizes, 'stock': total_stock, 'colors': colors, 'color_selected': color_selected, 'related_items': related_items}
    return render(request, 'store/product_detail.html', context)


def category_products(request, category):
    data = Product.objects.filter(
        category__slug=category).values('title', 'slug')
    print(f'data: {data}')
    context = {"data": data}
    return render(request, 'store/category_products.html', context)
