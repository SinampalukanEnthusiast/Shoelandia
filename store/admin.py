from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}


admin.site.register(Product, ProductAdmin)
# admin.site.register(ShippingAddress)
# admin.site.register(Customer)
# admin.site.register(Order)
# admin.site.register(OrderItem)
