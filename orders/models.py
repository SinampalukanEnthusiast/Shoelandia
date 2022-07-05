import email
from pyexpat import model
from django.conf import settings
from django.db import models
from decimal import Decimal
from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=9, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

# From previous system in app.store
# class Customer(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     customer = models.ForeignKey(
#         Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=True)
#     transaction_id = models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return str(self.id)

#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total

#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total


# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     @property
#     def get_total(self):
#         total = self.product.price * self.quantity
#         return total

#     def __str__(self):
#         myOrderItems = f"{self.product.product_name} {self.product.brand_name}"
#         return f'{myOrderItems}, {self.quantity}, '


# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(
#         Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     order = models.ForeignKey(
#         Order, on_delete=models.SET_NULL, null=True, blank=True)
#     address = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=200, null=True)
#     province = models.CharField(max_length=200, null=True)  # or region
#     zipcode = models.CharField(max_length=200, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address
