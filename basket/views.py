from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from requests import Session
from .basket import Basket
from store.models import Product, ProductImage


def basket_summary(request):
    basket = Basket(request)
    context = {'basket': basket}
    product_name = "Red Air Max"
    output = ProductImage.objects.filter(
        sub_product__sub_name=product_name).filter(is_feature=True).values('image')
    # print(output)
    return render(request, "basket/summary.html", context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'POST':

        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_size = str(request.POST.get('size'))
        product_variant = str(request.POST.get('variant'))
        product = get_object_or_404(Product, id=product_id)

        basket.add(product=product, qty=product_qty,
                   size=product_size, variant=product_variant)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})

        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_subtotal()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)

    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product=product_id, qty=product_qty)

        basket_qty = basket.__len__()
        basket_total = basket.get_subtotal()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response
