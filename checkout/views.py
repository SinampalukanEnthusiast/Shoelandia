
from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient
import json
import uuid
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from orders.models import Order, OrderItem

from .models import DeliveryOptions
from .forms import AddressCheckoutForm
from decimal import Decimal
from account.models import Addresses


@login_required
def deliverychoices(request):
    basket = request.session['basket']
    if basket:
        pass
    else:
        messages.success(request, "Please add items in your basket first.")
        return redirect('basket_summary')

    deliveryoptions = DeliveryOptions.objects.all()
    context = {"form": AddressCheckoutForm(),
               "deliveryoptions": deliveryoptions, 'session': request.session}

    return render(request, "checkout/delivery_choices.html", context)


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "POST":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(
            delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        if "delivery_selected" not in request.session:
            session["delivery_selected"] = {
                'delivery_selected': delivery_option
            }
        else:
            session["delivery_selected"] = delivery_option

        response = JsonResponse(
            {"total": updated_total_price, "delivery_price": delivery_type.delivery_price, })
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select a delivery option")
        return redirect("deliverychoices")

    address = Addresses.objects.filter(
        customer=request.user).order_by('-default')

    try:
        if "address" not in request.session:
            session["address"] = {'address_id': str(address[0].id)}
        else:
            session["address"]["address_id"] = str(address[0].id)
            session.modified = True
    except:
        address = None

    return render(request, "checkout/delivery_address.html", {"addresses": address})


@login_required
def payment_selection(request):
    address = Addresses.objects.filter(
        id=request.session["address"]['address_id'])
    basket = Basket(request)
    if "purchase" not in request.session:
        messages.success(request, "Please select a delivery option")
        return redirect("deliverychoices")
    else:
        return render(request, 'checkout/payment_selection.html', {'addresses': address})


@login_required
def payment_complete(request):
    session = request.session
    basket = Basket(request)
    PPClient = PayPalClient()
    address2 = ""
    city = ""
    phone = ""
    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id
    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)
    CURRENCY_CONVERSION = 40
    try:
        address2 = response.result.purchase_units[0].shipping.address.address_line_2
    except:
        address2 = ""
    try:
        city = response.result.purchase_units[0].shipping.address.admin_area_2
    except:
        city = ""

    total_paid = response.result.purchase_units[0].amount.value
    total_paid = round(Decimal(total_paid), 2)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=address2,
        city=city,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        phone=phone,
        total_paid=total_paid,
        order_key=response.result.id,
        payment_option="PayPal",
        billing_status=True,
    )

    order_id = order.pk

    for item in basket:
        price = item["price"]
        price = round(Decimal(price), 2)
        OrderItem.objects.create(
            order_id=order_id, product=item["product"], price=price, quantity=item["qty"], variant=item['variant'], size=item['size'])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", )


@login_required
def payment_complete_cod(request):
    basket = Basket(request)
    session = request.session
    address = Addresses.objects.filter(
        id=session["address"]['address_id']).values()

    user_id = request.user.id
    total_paid = basket.get_total_price()
    order_key = uuid.uuid4()
    country_code = "PH"

    for item in address:
        if item['full_name']:
            full_name = item['full_name']
        if item['phone']:
            phone = item['phone']
        if item['address_line']:
            address1 = item['address_line']
        if item['address_line2']:
            address2 = item['address_line2']
        if item['city']:
            city = item['city']
        if item['province']:
            province = item['province']
        if item['zipcode']:
            zipcode = item['zipcode']

    order = Order.objects.create(
        user_id=user_id,
        full_name=full_name,
        address1=address1,
        address2=address2,
        city=city,
        postal_code=zipcode,
        country_code=country_code,
        phone=phone,
        total_paid=total_paid,
        order_key=order_key,
        payment_option="Cash on Delivery (COD)",
        is_processing=True,
        billing_status=False, )
    order_id = order.pk
    for item in basket:
        price = item["price"]
        price = round(Decimal(price), 2)
        OrderItem.objects.create(
            order_id=order_id, product=item["product"], price=price, quantity=item["qty"], variant=item['variant'], size=item['size'])

    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_cod.html", {})
