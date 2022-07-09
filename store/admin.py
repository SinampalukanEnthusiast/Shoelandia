from django.contrib import admin
from .models import *
from django import forms
from mptt.admin import MPTTModelAdmin


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 0


class ProductSizesInline(admin.TabularInline):
    model = ProductSizes
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class SubProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizesInline, ProductColorInline, ProductImageInline]


class SubProductInline(admin.TabularInline):
    model = SubProduct
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SubProductInline, ]


class CategoryAttributeInline(admin.TabularInline):
    model = CategoryAttributes
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(SubProduct, SubProductAdmin)

admin.site.register(Category, MPTTModelAdmin)
# admin.site.register(CategoryAdmin)


# admin.site.register(CategoryAttributes, MPTTModelAdmin)
# admin.site.register(ProductSpecification)

# admin.site.register(ShippingAddress)
# admin.site.register(Customer)
# admin.site.register(Order)
# admin.site.register(OrderItem)
