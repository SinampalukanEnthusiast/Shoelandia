from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        verbose_name="Category Name",
        help_text="Required. Must be unique",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Category name url-safe", max_length=255, unique=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT)  # blank=True
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
        max_digits=8,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name="Discount price",
        max_digits=8,
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

    def get_subproducts(self):
        subproducts = self.subproduct_set.all()
        return subproducts

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
    is_default = models.BooleanField(verbose_name="Default subproduct",
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

    def get_sizes(self):
        sizes_queryset = self.productsizes_set.all()
        return sizes_queryset

    def get_images(self):
        images_queryset = self.product_image.all()
        return images_queryset

    def get_featured(self, images):
        for image in images:
            if image.is_feature:
                return image


class ProductSizes(models.Model):
    sub_product = models.ForeignKey(SubProduct, on_delete=models.RESTRICT)

    # Complete size choices
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

    @property
    def total_stock(self):
        return sum(self.stock_amount)

    def __str__(self):
        return f"{self.size}"


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
                             choices=COLOR_CHOICES, max_length=32, null=True, blank=False)

    def __str__(self):
        return f"{self.color} from {self.sub_product.sub_name}"


class ProductImage(models.Model):
    """
    The Subproduct Image table.
    """
    # make image required
    # make is feature required
    sub_product = models.ForeignKey(
        SubProduct, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name="image",
        help_text="Upload a product image",
        upload_to="",
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
