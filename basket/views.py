from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .basket import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    context = {'basket': basket}

    return render(request, "store/basket/summary.html", context)


def basket_add(request):
    basket = Basket(request)

    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})

        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
