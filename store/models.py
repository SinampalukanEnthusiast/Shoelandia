from itertools import product
from operator import mod
from tkinter import image_names
from turtle import ondrag
from unicodedata import category
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name="Category Name",
        help_text="Required. Must be unique",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Category safe URL", max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("category_list", args=[self.slug])

    def __str__(self):
        return self.name


class CategoryAttributes(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    attributes = models.CharField(
        max_length=255, help_text="Characteristics of the category.")


class AttributeValues(models.Model):
    category_attributes = models.ForeignKey(
        Category, on_delete=models.RESTRICT)
    values = models.CharField(
        max_length=255, help_text="Category attribute values.")


class Product(models.Model):
    """
    The Product table contining all product items.
    """
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name="title",
        help_text="Required",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="description", help_text="Not Required", blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name="Regular price",
        help_text="Maximum 999.99",
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999.99.",
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name="Discount price",
        help_text="Maximum 999.99",
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999.99.",
            },
        },
        max_digits=5,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name="Product visibility",
        help_text="Change product visibility",
        default=True,
    )
    created_at = models.DateTimeField(
        "Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def __str__(self):
        return self.title

    @property
    def get_full_name(self):
        return f'{self.title}'


class SubProduct(models.Model):

    sub_name = models.CharField(verbose_name="Subproduct Name",
                                help_text="Required. Sub-product Name", max_length=255)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True)

    brand = models.CharField(verbose_name="Brand Name",
                             help_text="Shoe brand. Not required.", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(verbose_name="Flagship subproduct",
                                     help_text="Is the main subproduct.",
                                     default=False)
    is_active = models.BooleanField(verbose_name="Subproduct visibility",
                                    help_text="Change subproduct visibility",
                                    default=True)

    class Meta:
        verbose_name = "Subproduct "
        verbose_name_plural = "Subproducts"

    def __str__(self):
        return self.sub_name


class ProductSizes(models.Model):
    sub_product = models.ForeignKey(SubProduct, on_delete=models.RESTRICT)

    SIZE_CHOICES = [("EU16", 8.1),
                    ("EU27", 16.1),
                    ("EU28", 16.6),
                    ("EU35", 21.2), ]

    size = models.CharField(verbose_name="Subproduct Size",
                            help_text="Sizes are in CM.", max_length=255, choices=SIZE_CHOICES)
    stock_amount = models.IntegerField(
        verbose_name="Stock amount.", help_text="Number of stock in inventory.", default=0)

    class Meta:
        verbose_name = "Product size "
        verbose_name_plural = "Product sizes"

    # @property
    # def total_size_stock(self):
    #     return self.sub_product.stock_amount

    def __str__(self):
        return f"{self.size} from {self.sub_product.sub_name}"


class ProductColor(models.Model):
    COLOR_CHOICES = [('RD', 'Red'),
                     ('BK', 'Black'),
                     ('BL', 'Blue'),
                     ('WT', 'White'),
                     ('BR', 'Brown'),
                     ('GR', 'Gray'),
                     ('OR', 'Orange'),
                     ('PN', 'Pink'), ]

    sub_product = models.OneToOneField(SubProduct, on_delete=models.RESTRICT)
    color = models.CharField(verbose_name="Subproduct Color",
                             choices=COLOR_CHOICES, max_length=32, null=True)
    stock_amount = models.IntegerField(
        verbose_name="Stock amount.", help_text="Number of stock in inventory.", default=0)

    def __str__(self):
        return f"{self.color} from {self.sub_product.sub_name}"


class ProductImage(models.Model):
    """
    The Subproduct Image table.
    """

    sub_product = models.ForeignKey(
        SubProduct, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name="image",
        help_text="Upload a product image",
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name="Alterrnative text",
        help_text="Please add alternative text",
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Subproduct Image"
        verbose_name_plural = "Subproduct Images"

    def __str__(self):
        return f"{self.sub_product.sub_name}"
