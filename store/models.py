from distutils.text_file import TextFile
from django.db import models
from django.contrib.auth.models import User
from django.forms import SlugField
from django.conf import settings


class Product(models.Model):
    product_name = models.CharField(max_length=200, null=True)
    brand_name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(max_length=255)
    # add color and size

    @property
    def get_full_name(self):
        return f'{self.brand_name} {self.product_name}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return f'{self.brand_name} {self.product_name}'
