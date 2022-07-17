from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 0


class ProductSizesInline(admin.TabularInline):
    model = ProductSizes
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class SubProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizesInline, ProductColorInline, ProductImageInline]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class AccountAdmin(admin.ModelAdmin):
    list_filter = ('user_name', 'email')


class SubProductInline(admin.TabularInline):
    model = SubProduct
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SubProductInline, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(SubProduct, SubProductAdmin)
admin.site.register(Category, CategoryAdmin)
