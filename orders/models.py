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
    phone = models.CharField(max_length=100)  # move down
    # province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=9, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(
        default=False, verbose_name="Payment Status")
    #is_processing = models.BooleanField(default=False, verbose_name="Processing Status")
    #is_delivered = models.BooleanField(default=False, verbose_name="Delivery Status")
    #is_returned = models.BooleanField(default=False, verbose_name="Return Status")
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
    #variant = models.CharField(max_length=50, blank=True, verbose_name="Product Variant")
    #size = models.CharField(max_length=50, blank=True, verbose_name="Product Size")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
