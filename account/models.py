import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('...Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                '...Superuser must be assigned to is_superuser=True')
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=150,)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    association = models.CharField(
        max_length=150, verbose_name="Association", help_text="Company the user belongs to.")

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Addresses(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Customer")
    full_name = models.CharField(max_length=150, )
    phone = models.CharField(max_length=20, blank=True)  # blank=True
    zipcode = models.CharField(max_length=150, blank=True)  # blank=True
    address_line = models.CharField(
        max_length=255, verbose_name="Address Line 1")
    address_line2 = models.CharField(
        max_length=255, verbose_name="Address Line 2")

    city = models.CharField(
        max_length=150, verbose_name="City or Municipality")
    province = models.CharField(
        max_length=150, verbose_name="Province or Region")
    delivery_instructions = models.TextField(
        max_length=255, blank=True)  # blank=True
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True)
    default = models.BooleanField(
        default=False, verbose_name="Default Address", blank=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'Address: {self.customer} {self.created}'
