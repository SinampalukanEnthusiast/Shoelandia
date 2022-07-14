
from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient
from datetime import datetime
import json
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from orders.models import Order, OrderItem

from .models import DeliveryOptions
from .forms import AddressCheckoutForm
from decimal import Decimal


@login_required
def deliverychoices(request):
    basket = request.session['basket']
    if basket:
        pass
    else:
        messages.success(request, "Please add items in your basket first.")
        return redirect('basket_summary')

    deliveryoptions = DeliveryOptions.objects.all()
    print(deliveryoptions)
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
    address = {"full_name": "Junnie Beaue",
               "phone": "12345678910",
               "postcode": "2031",
               "address_line": "add 1",
               "address_line2": "add 2",
               "town_city": "San Nico mf",
               "delivery_instructions": "Instructions",
               "created_at": datetime.now(),
               "updated_at": datetime.now(),
               "default": True,
               }

    return render(request, "checkout/delivery_address.html", {"addresses": address})


@login_required
def payment_selection(request):
    if "purchase" not in request.session:
        messages.success(request, "Please select a delivery option")
        return redirect("deliverychoices")
    else:
        return render(request, 'checkout/payment_selection.html', {})


@login_required
def payment_complete(request):
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
        payment_option="paypal",
        billing_status=True,
    )

    order_id = order.pk

    for item in basket:
        price = item["price"]
        price = round(Decimal(price), 2)
        OrderItem.objects.create(
            order_id=order_id, product=item["product"], price=price, quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
